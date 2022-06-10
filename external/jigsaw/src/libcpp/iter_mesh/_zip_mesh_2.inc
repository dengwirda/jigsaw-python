
    /*
    --------------------------------------------------------
     * _ZIP-MESH-2: merge/split operations.
    --------------------------------------------------------
     *
     * This program may be freely redistributed under the
     * condition that the copyright notices (including this
     * entire header) are not removed, and no compensation
     * is received through use of the software.  Private,
     * research, and institutional use is free.  You may
     * distribute modified versions of this code UNDER THE
     * CONDITION THAT THIS CODE AND ANY MODIFICATIONS MADE
     * TO IT IN THE SAME FILE REMAIN UNDER COPYRIGHT OF THE
     * ORIGINAL AUTHOR, BOTH SOURCE AND OBJECT CODE ARE
     * MADE FREELY AVAILABLE WITHOUT CHARGE, AND CLEAR
     * NOTICE IS GIVEN OF THE MODIFICATIONS.  Distribution
     * of this code as part of a commercial system is
     * permissible ONLY BY DIRECT ARRANGEMENT WITH THE
     * AUTHOR.  (If you are not directly supplying this
     * code to a customer, and you are instead telling them
     * how they can obtain it for free, then you are not
     * required to make any arrangement with me.)
     *
     * Disclaimer:  Neither I nor: Columbia University, The
     * Massachusetts Institute of Technology, The
     * University of Sydney, nor The National Aeronautics
     * and Space Administration warrant this code in any
     * way whatsoever.  This code is provided "as-is" to be
     * used at your own risk.
     *
    --------------------------------------------------------
     *
     * Last updated: 10 Jun., 2022
     *
     * Copyright 2013-2022
     * Darren Engwirda
     * d.engwirda@gmail.com
     * https://github.com/dengwirda/
     *
    --------------------------------------------------------
     */

    // from item_mesh_2.hpp


    /*
    --------------------------------------------------------
     * _ZIP-MESH: edge merge/split operations.
    --------------------------------------------------------
     */

    #include "iter_zips_2.inc"
    #include "iter_divs_2.inc"

    __static_call
    __normal_call void_type _zip_mesh (
        geom_type &_geom ,
        mesh_type &_mesh ,
        hfun_type &_hfun ,
        char_type  _kern ,
        real_list &_hval ,
        iptr_list &_nset ,
        mark_list &_mark ,
        iptr_type  _imrk ,
        iter_opts &_opts ,
        real_type  _QLIM ,
        real_type  _DLIM ,
        iptr_type &_nzip ,
        iptr_type &_ndiv ,
        iter_stat &_tcpu
        )
    {
        class sort_pair
            {
            public  :
    /*------------------------ tuple for edge re-ordering */
            iptr_type           _inod ;
            iptr_type           _jnod ;
            float               _cost ;
            public  :
            __inline_call sort_pair (
                iptr_type _isrc ,
                iptr_type _jsrc ,
                float     _csrc
                ) : _inod(_isrc), _jnod(_jsrc),
                    _cost(_csrc)   {}
            } ;
        class sort_less
            {
            public  :
    /*------------------------ less-than op. for cost-tup */
            __inline_call
                bool_type operator () (
                sort_pair const&_idat ,
                sort_pair const&_jdat
                ) const
            {  return  _idat._cost < _jdat._cost;
            }
            } ;

    #   define MARKNODE(_NODE) _mark._node[_NODE]

    #   define PUSHMARK              \
            init_mark( _mesh, _mark,        \
                std::max(_imrk - 1, +0));   \
            if (std::abs(           \
                _mark._node[_nnew])!= _imrk+1)  \
            {                       \
            if (_mark._node[_nnew] >= +0)   \
            {                       \
                _mark._node[_nnew] = +_imrk+1;  \
            }                       \
            else                    \
            {                       \
                _mark._node[_nnew] = -_imrk-1;  \
            }                       \
                _nset.push_tail(_nnew) ;    \
            }                       \

    /*------------------------ add/pop nodes to fix topo. */
        typedef containers::
            array<sort_pair> sort_list ;

        __unreferenced ( _DLIM );

        sort_list _sort ;
        conn_list _aset , _bset, _cset ;
        conn_list _conn , _iset, _jset ;
        real_list _qold , _qnew, _qtmp ;

        _nzip = +0 ; _ndiv = +0 ;

    //  assemble list of edges attached to "recent" nodes

        _sort.set_alloc(
            _mesh.edge().count()) ;

        for (auto _iter  = _mesh.edge().head() ;
                  _iter != _mesh.edge().tend() ;
                ++_iter  )
        {
             auto _inod =  _iter->node(0) ;
             auto _jnod =  _iter->node(1) ;

             auto _iptr = _mesh.
             node().head()+_iter->node(0) ;
             auto _jptr = _mesh.
             node().head()+_iter->node(1) ;

             auto _flag = _imrk - 2 ; // recent

            if (_iter->mark() >= +0 &&
               (    std::abs(
                _mark._node[_inod]) > _flag ||
                    std::abs(
                _mark._node[_jnod]) > _flag ))
            {
                float _lsqr  =
               (float)pred_type::length_sq (
                    & _iptr->pval(0) ,
                    & _jptr->pval(0) ) ;

                _sort.push_tail(
                 sort_pair(_inod, _jnod, _lsqr)) ;
            }
        }

        if (_sort.empty()) return ;

        algorithms::qsort(      // sort edge list by lsqr
            _sort.head() ,
            _sort.tend() , sort_less());

    //  scan edges longest-to-shortest and try to div any
    //  unvisited edges

        for (auto _iter  = _sort.tail();
                  _iter != _sort.hend();
                --_iter  )
        {
    /*--------------------------- try to "div" local edge */
            iptr_type  _eadj, _enod[2] ;
            _enod[0] = _iter->_inod;
            _enod[1] = _iter->_jnod;

            if (MARKNODE(_enod[0]) < +0 &&
                MARKNODE(_enod[1]) < +0 ) continue ;

            if (MARKNODE(_enod[0])>_imrk||
                MARKNODE(_enod[1])>_imrk) continue ;

            if(!_mesh.find_edge(
                          _enod, _eadj) ) continue ;

            if (_opts.div_())
            {
    /*--------------------------- "div" for topo. + score */
                iptr_type  _nnew = -1;

                bool_type  _move = false ;
                _div_edge( _geom, _mesh,
                    _hfun, _hval, _opts,
                    _imrk, _eadj,
                    _kern, _move, _nnew,
                    _iset, _jset,
                    _aset, _bset,
                    _qold, _qnew,
                    _qtmp, _QLIM, _tcpu) ;

                if (_move)
                {
                    PUSHMARK; _ndiv += +1;
                }
            }
        }

    //  scan edges shortest-to-longest and try to zip any
    //  unvisited edges

        for (auto _iter  = _sort.head();
                  _iter != _sort.tend();
                ++_iter  )
        {
    /*--------------------------- try to "zip" local edge */
            iptr_type  _eadj, _enod[2] ;
            _enod[0] = _iter->_inod;
            _enod[1] = _iter->_jnod;

            if (MARKNODE(_enod[0]) < +0 ||
                MARKNODE(_enod[1]) < +0 ) continue ;

            if (MARKNODE(_enod[0])>_imrk||
                MARKNODE(_enod[1])>_imrk) continue ;

            if(!_mesh.find_edge(
                          _enod, _eadj) ) continue ;

            if (_opts.zip_())
            {
    /*--------------------------- "zip" for topo. + score */
                iptr_type  _nnew = -1;

                bool_type  _move = false ;
                _zip_edge( _geom, _mesh,
                    _hfun, _hval, _opts,
                    _mark. _node,
                    _imrk, _eadj,
                    _kern, _move, _nnew,
                    _iset, _jset,
                    _aset, _bset, _cset,
                    _qold, _qnew,
                    _qtmp, _QLIM, _tcpu) ;

                if (_move)
                {
                    PUSHMARK; _nzip += +1;
                }
            }
        }

        for (auto _iter  = _mark._node.head() ;
                  _iter != _mark._node.tend() ;
                ++_iter  )
        {
    /*--------------------- undo local inc. on node flags */
            if (*_iter > + _imrk)
                *_iter = + _imrk;
            else
            if (*_iter < - _imrk)
                *_iter = - _imrk;
        }

    #   undef   PUSHMARK
    #   undef   MARKNODE
    }



