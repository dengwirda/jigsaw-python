
    /*
    --------------------------------------------------------
     * FLIP-MESH-2: update mesh topologies.
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
     * FLIP-TRI3: "flip" mesh topology.
    --------------------------------------------------------
     */

    __static_call
    __inline_call void_type flip_tri3 (
        geom_type &_geom ,
        mesh_type &_mesh ,
        iptr_list &_nmrk ,
        iptr_type  _cell ,
        bool_type &_flip ,
        conn_list &_conn ,
        conn_list &_next ,
        real_list &_qold ,
        real_list &_qnew ,
        flip_kind  _kind
        )
    {
        auto _coin = (std::rand() % 3) + 1  ;
        for (auto _enum = _coin; _enum-- > 0; )
        {
            _flip = false ;
    /*----------------------------- flip cells about edge */
            iptr_type _enod[3] ;
            mesh_type::tri3_type::
            face_node(_enod, _enum, +2, +1) ;
            _enod[ 0] = _mesh.tri3(
                _cell).node( _enod[ 0]) ;
            _enod[ 1] = _mesh.tri3(
                _cell).node( _enod[ 1]) ;

            _conn.set_count(0) ;
            _next.set_count(0) ;
            _mesh.connect_2(
               &_enod[0], EDGE2_tag, _conn) ;

            if (_conn.count() != +2) continue ;

            if (_conn[0]._kind==TRIA3_tag &&
                _conn[1]._kind==TRIA3_tag )
            {
                flip_t2t2( _geom, _mesh, _nmrk, _enod,
                    _conn, _next, _flip,
                    _qold, _qnew, _kind)  ;

                if (_flip) return ;
            }
            else
            {
            //  flip_t1q1( _geom, _mesh, _nmrk, _enod,
            //      _conn, _next, _flip,
            //      _qold, _qnew, _kind)  ;

                if (_flip) return ;
            }
        }

        for (auto _enum = 3; _enum-- > _coin; )
        {
            _flip = false ;
    /*----------------------------- flip cells about edge */
            iptr_type _enod[3] ;
            mesh_type::tri3_type::
            face_node(_enod, _enum, +2, +1) ;
            _enod[ 0] = _mesh.tri3(
                _cell).node( _enod[ 0]) ;
            _enod[ 1] = _mesh.tri3(
                _cell).node( _enod[ 1]) ;

            _conn.set_count(0) ;
            _next.set_count(0) ;
            _mesh.connect_2(
               &_enod[0], EDGE2_tag, _conn) ;

            if (_conn.count() != +2) continue ;

            if (_conn[0]._kind==TRIA3_tag &&
                _conn[1]._kind==TRIA3_tag )
            {
                flip_t2t2( _geom, _mesh, _nmrk, _enod,
                    _conn, _next, _flip,
                    _qold, _qnew, _kind)  ;

                if (_flip) return ;
            }
            else
            {
            //  flip_t1q1( _geom, _mesh, _nmrk, _enod,
            //      _conn, _next, _flip,
            //      _qold, _qnew, _kind)  ;

                if (_flip) return ;
            }
        }

    }

    /*
    --------------------------------------------------------
     * FLIP-QUAD: "flip" mesh topology.
    --------------------------------------------------------
     */

    __static_call
    __inline_call void_type flip_quad (
        geom_type &/*_geom*/ ,
        mesh_type &_mesh ,
        iptr_list &_nmrk ,
        iptr_type  _cell ,
        bool_type &_flip ,
        conn_list &_conn ,
        conn_list &_next ,
        real_list &/*_qold*/ ,
        real_list &/*_qnew*/ ,
        flip_kind  /*_kind*/
        )
    {
        auto _coin = (std::rand() % 4) + 1  ;
        for (auto _enum = _coin; _enum-- > 0; )
        {
            _flip = false ;
    /*----------------------------- flip cells about edge */
            iptr_type _enod[4] ;
            mesh_type::quad_type::
            face_node(_enod, _enum, +2, +1) ;
            _enod[ 0] = _mesh.quad(
                _cell).node( _enod[ 0]) ;
            _enod[ 1] = _mesh.quad(
                _cell).node( _enod[ 1]) ;

            _conn.set_count(0) ;
            _next.set_count(0) ;
            _mesh.connect_2(
               &_enod[0], EDGE2_tag, _conn) ;

            if (_conn.count() != +2) continue ;

            if (_conn[0]._kind==QUAD4_tag &&
                _conn[1]._kind==QUAD4_tag )
            {
            //  flip_q2q2( _geom, _mesh, _enod, _nmrk,
            //      _conn, _next, _flip,
            //      _qold, _qnew, _kind)  ;

                if (_flip) return ;
            }
            else
            {
            //  flip_t1q1( _geom, _mesh, _enod, _nmrk,
            //      _conn, _next, _flip,
            //      _qold, _qnew, _kind)  ;

                if (_flip) return ;
            }
        }

        for (auto _enum = 4; _enum-- > _coin; )
        {
            _flip = false ;
    /*----------------------------- flip cells about edge */
            iptr_type _enod[4] ;
            mesh_type::quad_type::
            face_node(_enod, _enum, +2, +1) ;
            _enod[ 0] = _mesh.quad(
                _cell).node( _enod[ 0]) ;
            _enod[ 1] = _mesh.quad(
                _cell).node( _enod[ 1]) ;

            _conn.set_count(0) ;
            _next.set_count(0) ;
            _mesh.connect_2(
               &_enod[0], EDGE2_tag, _conn) ;

            if (_conn.count() != +2) continue ;

            if (_conn[0]._kind==QUAD4_tag &&
                _conn[1]._kind==QUAD4_tag )
            {
            //  flip_q2q2( _geom, _mesh, _enod, _nmrk,
            //      _conn, _next, _flip,
            //      _qold, _qnew, _kind)  ;

                if (_flip) return ;
            }
            else
            {
            //  flip_t1q1( _geom, _mesh, _enod, _nmrk,
            //      _conn, _next, _flip,
            //      _qold, _qnew, _kind)  ;

                if (_flip) return ;
            }
        }

    }

    /*
    --------------------------------------------------------
     * FLIP-MESH: "flip" mesh topology.
    --------------------------------------------------------
     */

    #include "iter_flip_2.inc"

    __static_call
    __normal_call void_type flip_mesh (
        geom_type &_geom ,
        mesh_type &_mesh ,
        hfun_type &_hfun ,
        iptr_list &_nset ,
        mark_list &_mark ,
        iptr_type  _imrk ,
        iptr_type &_nflp
        )
    {
    #   define MARKTRI3(_CELL) \
                _mark._tri3[_CELL->_cell]

    #   define MARKQUAD(_CELL) \
                _mark._quad[_CELL->_cell]

        init_mark(_mesh, _mark ,
            std::max(+0, _imrk - 1) ) ;

        _nflp = +0 ;

        conn_list _flip, _conn ;

    /*--------------------- init. flip stack as ADJ(NSET) */
        for (auto _iter  = _nset.head();
                  _iter != _nset.tend();
                ++_iter  )
        {
            if (_mesh.node(*_iter).mark() >= 0)
            {
                _conn.set_count(0);
                _mesh.connect_2(
                  &*_iter, POINT_tag, _conn) ;

                for (auto _cell  = _conn.head();
                          _cell != _conn.tend();
                        ++_cell  )
                {
                if (_cell->_kind == TRIA3_tag)
                {
                if (MARKTRI3( _cell ) != _imrk)
                {
                    MARKTRI3( _cell )  = _imrk ;

                    _flip.push_tail( *_cell) ;
                }
                }
                else
                if (_cell->_kind == QUAD4_tag)
                {
                if (MARKQUAD( _cell ) != _imrk)
                {
                    MARKQUAD( _cell )  = _imrk ;

                    _flip.push_tail( *_cell) ;
                }
                }
                }
            }
        }

        flip_core(_geom, _mesh, _hfun, _flip, _mark,
            _nflp) ;

    #   undef   MARKQUAD
    #   undef   MARKTRI3
    }

    __static_call
    __normal_call void_type flip_mesh (
        geom_type &_geom ,
        mesh_type &_mesh ,
        hfun_type &_hfun ,
        conn_sets &_CONN ,
        iptr_list &_nset ,
        mark_list &_mark ,
        iptr_type  _imrk ,
        iptr_type &_nflp
        )
    {
    #   define MARKTRI3(_CELL) \
                _mark._tri3[_CELL->_cell]

    #   define MARKQUAD(_CELL) \
                _mark._quad[_CELL->_cell]

        init_mark(_mesh, _mark ,
            std::max(+0, _imrk - 1) ) ;

        _nflp = +0 ;

        conn_list _flip  ;

    /*--------------------- init. flip stack as ADJ(NSET) */
        for (auto _iter  = _nset.head();
                  _iter != _nset.tend();
                ++_iter  )
        {
            if (_mesh.node(*_iter).mark() >= 0)
            {
                for (auto _cell  =
            _CONN._adj2.head()+_CONN._idx2[*_iter+0] ;
                          _cell !=
            _CONN._adj2.head()+_CONN._idx2[*_iter+1] ;
                        ++_cell  )
                {
                if (_cell->_kind == TRIA3_tag)
                {
                if (MARKTRI3( _cell ) != _imrk)
                {
                    MARKTRI3( _cell )  = _imrk ;

                    _flip.push_tail( *_cell) ;
                }
                }
                else
                if (_cell->_kind == QUAD4_tag)
                {
                if (MARKQUAD( _cell ) != _imrk)
                {
                    MARKQUAD( _cell )  = _imrk ;

                    _flip.push_tail( *_cell) ;
                }
                }
                }
            }
        }

        flip_core(_geom, _mesh, _hfun, _flip, _mark,
            _nflp) ;

    #   undef   MARKQUAD
    #   undef   MARKTRI3
    }

    __static_call
    __normal_call void_type flip_core (
        geom_type &_geom ,
        mesh_type &_mesh ,
        hfun_type &_hfun ,
        conn_list &_flip ,
        mark_list &_mark ,
        iptr_type &_nflp
        )
    {
        __unreferenced ( _hfun ) ;

    /*--------------------- exhaustive, incremental flips */
        conn_list _next, _conn, _CONN;
        real_list _qold, _qnew ;
        for ( ; !_flip.empty() ; )
        {
        for (auto _cell  = _flip.head();
                  _cell != _flip.tend();
                ++_cell  )
        {
            if (_cell->_kind == TRIA3_tag)
            {
            if (  _mesh.
                tri3(_cell->_cell).mark() >= +0)
            {
                bool_type  _okay = false ;
                flip_tri3( _geom, _mesh,
                    _mark. _node,
                    _cell->_cell,
                    _okay, _conn, _CONN,
                    _qold, _qnew,
               (flip_kind)laguerre_flip) ;

                if (_okay) _nflp += +1 ;

                _next.push_tail(
                    _CONN.head(), _CONN.tend());
            }
            }
            else
            if (_cell->_kind == QUAD4_tag)
            {
            if (  _mesh.
                quad(_cell->_cell).mark() >= +0)
            {
                bool_type  _okay = false ;
              //flip_quad( _geom, _mesh,
              //    _mark. _node,
              //    _cell->_cell,
              //    _okay, _conn, _CONN,
              //    _qold, _qnew,
            // (flip_kind)laguerre_flip) ;

                if (_okay) _nflp += +1 ;

                _next.push_tail(
                    _CONN.head(), _CONN.tend());
            }
            }
        }
            _flip = std::move (_next) ;
        }
    }



