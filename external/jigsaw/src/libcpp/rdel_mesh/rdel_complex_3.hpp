
    /*
    --------------------------------------------------------
     * RDEL-COMPLEX-3: restricted delaunay obj. in R^3.
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
     * Disclaimer:  Neither I nor THE CONTRIBUTORS warrant
     * this code in any way whatsoever.  This code is
     * provided "as-is" to be used at your own risk.
     *
     * THE CONTRIBUTORS include:
     * (a) The University of Sydney
     * (b) The Massachusetts Institute of Technology
     * (c) Columbia University
     * (d) The National Aeronautics & Space Administration
     * (e) Los Alamos National Laboratory
     *
    --------------------------------------------------------
     *
     * Last updated: 02 Aug., 2022
     *
     * Copyright 2013-2022
     * Darren Engwirda
     * d.engwirda@gmail.com
     * https://github.com/dengwirda/
     *
    --------------------------------------------------------
     */

#   pragma once

#   ifndef __RDEL_COMPLEX_3__
#   define __RDEL_COMPLEX_3__

    namespace mesh {

    template <
    typename R,
    typename I
             >
    class rdel_complex_3d
    {
    public  :

    /*--------------- restricted delauany-tri obj. in R^3 */

    typedef R                       real_type;
    typedef I                       iptr_type;

    typedef mesh::laguerre_tri_node_3 <
            iptr_type ,
            real_type >             tria_node_base ;

    typedef mesh::laguerre_tri_tria_3 <
            iptr_type ,
            real_type >             tria_tria_base ;

    class tria_node : public tria_node_base
        {
        public  :
    /*---------------------------- delaunay-tri node type */
            iptr_type     _idxh = 0 ;
            iptr_type     _part = 0 ;

            char_type     _fdim = 0 ;

            char_type     _feat = 0 ;

            char_type     _topo [ 2] = {+2} ;

        public  :

        __inline_call iptr_type      & idxh (
            )
        {   return  this->_idxh ;
        }
        __inline_call iptr_type const& idxh (
            ) const
        {   return  this->_idxh ;
        }
        __inline_call iptr_type      & part (
            )
        {   return  this->_part ;
        }
        __inline_call iptr_type const& part (
            ) const
        {   return  this->_part ;
        }
        __inline_call char_type      & fdim (
            )
        {   return  this->_fdim ;
        }
        __inline_call char_type const& fdim (
            ) const
        {   return  this->_fdim ;
        }
        __inline_call char_type      & feat (
            )
        {   return  this->_feat ;
        }
        __inline_call char_type const& feat (
            ) const
        {   return  this->_feat ;
        }
        __inline_call char_type      & topo (
            char_type _kind = filt_topo
            )
        {   return ( _kind == filt_topo ) ?
                    this->_topo[ +0] :
                    this->_topo[ +1] ;
        }
        __inline_call char_type const& topo (
            char_type _kind = filt_topo
            ) const
        {   return ( _kind == filt_topo ) ?
                    this->_topo[ +0] :
                    this->_topo[ +1] ;
        }
        } ;

        class tria_tria : public tria_tria_base
        {
        public  :
    /*---------------------------- delaunay-tri tria type */
            real_type    _circ[  +3] ;

        public  :

        __inline_call real_type      & circ (
            iptr_type _ipos
            )
        {
            return this->_circ[ _ipos] ;
        }
        __inline_call real_type const& circ (
            iptr_type _ipos
            ) const
        {   return this->_circ[ _ipos] ;
        }
        } ;

    typedef mesh::laguerre_tri_euclidean_3  <
                iptr_type ,
                real_type >       tria_core ;

    typedef mesh::delaunay_tri_k    <
                tria_node ,
                tria_tria ,
                tria_core >       tria_type ;

    #define __hashscal sizeof(iptr_type)/sizeof(uint32_t)

    class node_data
        {
        public  :
    /*---------------------------------------- node nodes */
        containers::
        fixed_array<iptr_type, +1>  _node;

        iptr_type                   _pass;

        iptr_type                   _tadj;
        } ;

    class ball_data
        {
        public  :
    /*---------------------------------------- ball radii */
        containers::
        fixed_array<real_type, +4>  _ball;

        containers::
        fixed_array<iptr_type, +1>  _node;

        iptr_type                   _pass;

        char_type                   _kind;
        } ;

    class edge_data
        {
        public  :
    /*---------------------------------------- edge nodes */
        containers::
        fixed_array<iptr_type, +2>  _node;

        iptr_type                   _pass;
        iptr_type                   _part;
        char_type                   _kind;

        char_type                   _feat;
        char_type                   _topo[ 2];

        char_type                   _eadj;
        iptr_type                   _tadj;
        } ;

    class face_data
        {
        public  :
    /*---------------------------------------- face nodes */
        containers::
        fixed_array<iptr_type, +3>  _node;

        iptr_type                   _pass;
        iptr_type                   _part;
        char_type                   _kind;

        char_type                   _dups; // temp. counter
                                           // note: packing

        char_type                   _fadj;
        iptr_type                   _tadj;
        } ;

    class tria_data
        {
        public  :
    /*---------------------------------------- tria nodes */
        containers::
        fixed_array<iptr_type, +4>  _node;

        iptr_type                   _pass;
        iptr_type                   _part;
        char_type                   _kind;

        iptr_type                   _tadj;
        } ;

    class node_hash
        {
        public  :
        __inline_call uint32_t  operator() (
            node_data const&_ndat
            ) const
        {
    /*----------------------- hash node indexing for node */
            return hash::hashword (
                (uint32_t*)&_ndat._node[0],
                    +1 * __hashscal, +137);
        }
        } ;
    class ball_hash
        {
    /*----------------------- hash node indexing for ball */
        public  :
        __inline_call uint32_t  operator() (
            ball_data const&_bdat
            ) const
        {
            return hash::hashword (
                (uint32_t*)&_bdat._node[0],
                    +1 * __hashscal, +137);
        }
        } ;
    class edge_hash
        {
        public  :
        __inline_call uint32_t  operator() (
            edge_data const&_edat
            ) const
        {
    /*----------------------- hash node indexing for edge */
            return hash::hashword (
                (uint32_t*)&_edat._node[0],
                    +2 * __hashscal, +137);
        }
        } ;
    class face_hash
        {
        public  :
        __inline_call uint32_t  operator() (
            face_data const&_fdat
            ) const
        {
    /*----------------------- hash node indexing for face */
            return hash::hashword (
                (uint32_t*)&_fdat._node[0],
                    +3 * __hashscal, +137);
        }
        } ;
    class tria_hash
        {
        public  :
        __inline_call uint32_t  operator() (
            tria_data const&_tdat
            ) const
        {
    /*----------------------- hash node indexing for tria */
            return hash::hashword (
                (uint32_t*)&_tdat._node[0],
                    +4 * __hashscal, +137);
        }
        } ;

    class node_pred
        {
        public  :
        __inline_call bool_type operator() (
            node_data const&_idat,
            node_data const&_jdat
            ) const
        {
    /*------------------------------- "equal-to" for node */
            return _idat._node[0] ==
                   _jdat._node[0]  ;
        }
        } ;
    class ball_pred
        {
    /*------------------------------- "equal-to" for ball */
        public  :
        __inline_call bool_type operator() (
            ball_data const&_idat ,
            ball_data const&_jdat
            ) const
        {
            return _idat._node[0] ==
                   _jdat._node[0] &&
                   _idat._kind    ==
                   _jdat._kind    ;
        }
        } ;
    class edge_pred
        {
        public  :
        __inline_call bool_type operator() (
            edge_data const&_idat,
            edge_data const&_jdat
            ) const
        {
    /*------------------------------- "equal-to" for edge */
            return _idat._node[0] ==
                   _jdat._node[0] &&
                   _idat._node[1] ==
                   _jdat._node[1]  ;
        }
        } ;
    class face_pred
        {
        public  :
        __inline_call bool_type operator() (
            face_data const&_idat,
            face_data const&_jdat
            ) const
        {
    /*------------------------------- "equal-to" for face */
            return _idat._node[0] ==
                   _jdat._node[0] &&
                   _idat._node[1] ==
                   _jdat._node[1] &&
                   _idat._node[2] ==
                   _jdat._node[2]  ;
        }
        } ;
    class tria_pred
        {
        public  :
        __inline_call bool_type operator() (
            tria_data const&_idat,
            tria_data const&_jdat
            ) const
        {
    /*------------------------------- "equal-to" for tria */
            return _idat._node[0] ==
                   _jdat._node[0] &&
                   _idat._node[1] ==
                   _jdat._node[1] &&
                   _idat._node[2] ==
                   _jdat._node[2] &&
                   _idat._node[3] ==
                   _jdat._node[3] ;
        }
        } ;

    #undef  __hashscal

    iptr_type static
        constexpr pool_byte_size = 96 * 1024 ;

    typedef allocators::_pool_alloc <
            allocators::basic_alloc ,
            pool_byte_size          >   pool_base ;
    typedef allocators::_wrap_alloc <
                pool_base>              pool_wrap ;

    typedef containers::hash_table  <
                node_data,
                node_hash,
                node_pred,
                pool_wrap>              node_list ;
    typedef containers::hash_table  <
                ball_data,
                ball_hash,
                ball_pred,
                pool_wrap>              ball_list ;
    typedef containers::hash_table  <
                edge_data,
                edge_hash,
                edge_pred,
                pool_wrap>              edge_list ;
    typedef containers::hash_table  <
                face_data,
                face_hash,
                face_pred,
                pool_wrap>              face_list ;
    typedef containers::hash_table  <
                tria_data,
                tria_hash,
                tria_pred,
                pool_wrap>              tria_list ;

    typedef typename
            node_list::item_type        node_item ;
    typedef typename
            ball_list::item_type        ball_item ;
    typedef typename
            edge_list::item_type        edge_item ;
    typedef typename
            face_list::item_type        face_item ;
    typedef typename
            tria_list::item_type        tria_item ;

    public  :
    tria_type                   _tria ;

    pool_base                   _npol ;
    pool_base                   _bpol ;
    pool_base                   _epol, _e2nd ;
    pool_base                   _fpol, _f2nd ;
    pool_base                   _tpol ;

    node_list                   _nset ;
    ball_list                   _bset ;
    edge_list                   _eset, _etwo ;
    face_list                   _fset, _ftwo ;
    tria_list                   _tset ;

    public  :

    __inline_call rdel_complex_3d (
        //tria_type const& _tsrc = tria_type()
        ) : _npol(
        sizeof(typename node_list::item_type)) ,
            _bpol(
        sizeof(typename ball_list::item_type)) ,
            _epol(
        sizeof(typename edge_list::item_type)) ,
            _e2nd(
        sizeof(typename edge_list::item_type)) ,
            _fpol(
        sizeof(typename face_list::item_type)) ,
            _f2nd(
        sizeof(typename face_list::item_type)) ,
            _tpol(
        sizeof(typename tria_list::item_type)) ,

        _nset(node_hash(),
              node_pred(),
        +.8, (pool_wrap(&_npol))) ,
        _bset(ball_hash(),
              ball_pred(),
        +.8, (pool_wrap(&_bpol))) ,
        _eset(edge_hash(),
              edge_pred(),
        +.8, (pool_wrap(&_epol))) ,
        _etwo(edge_hash(),
              edge_pred(),
        +.8, (pool_wrap(&_e2nd))) ,
        _fset(face_hash(),
              face_pred(),
        +.8, (pool_wrap(&_fpol))) ,
        _ftwo(face_hash(),
              face_pred(),
        +.8, (pool_wrap(&_f2nd))) ,
        _tset(tria_hash(),
              tria_pred(),
        +.8, (pool_wrap(&_tpol)))
    {
    }

    __inline_call~rdel_complex_3d (
        )
    {
        clear (containers::tight_alloc);
    }

    __normal_call void_type clear (
        containers::alloc_types _alloc =
        containers::loose_alloc
        )
    {
        this->_tria.clear(_alloc) ;

        this->_nset.clear(_alloc) ;
        this->_npol.clear()  ;

        this->_bset.clear(_alloc) ;
        this->_bpol.clear()  ;

        this->_eset.clear(_alloc) ;
        this->_epol.clear()  ;

        this->_fset.clear(_alloc) ;
        this->_fpol.clear()  ;

        this->_tset.clear(_alloc) ;
        this->_tpol.clear()  ;
    }

    __inline_call
    typename ball_list::_write_it push_ball (
        ball_data const&_bdat
        )
    {   return this->_bset.push(_bdat);
    }
    __inline_call
    typename edge_list::_write_it push_edge (
        edge_data const&_edat
        )
    {   return this->_eset.push(_edat);
    }
    __inline_call
    typename face_list::_write_it push_face (
        face_data const&_fdat
        )
    {   return this->_fset.push(_fdat);
    }
    __inline_call
    typename tria_list::_write_it push_tria (
        tria_data const&_tdat
        )
    {   return this->_tset.push(_tdat);
    }

    __inline_call bool_type _pop_ball (
        ball_data const&_bdat,
        ball_data      &_same
        )
    {   return this->_bset._pop(_bdat, _same);
    }
    __inline_call bool_type _pop_edge (
        edge_data const&_edat,
        edge_data      &_same
        )
    {   return this->_eset._pop(_edat, _same);
    }
    __inline_call bool_type _pop_face (
        face_data const&_fdat,
        face_data      &_same
        )
    {   return this->_fset._pop(_fdat, _same);
    }
    __inline_call bool_type _pop_tria (
        tria_data const&_tdat,
        tria_data      &_same
        )
    {   return this->_tset._pop(_tdat, _same);
    }

    __inline_call bool_type _pop_ball (
        ball_data const&_bdat
        )
    {   return this->_bset._pop(_bdat);
    }
    __inline_call bool_type _pop_edge (
        edge_data const&_edat
        )
    {   return this->_eset._pop(_edat);
    }
    __inline_call bool_type _pop_face (
        face_data const&_fdat
        )
    {   return this->_fset._pop(_fdat);
    }
    __inline_call bool_type _pop_tria (
        tria_data const&_tdat
        )
    {   return this->_tset._pop(_tdat);
    }

    __inline_call bool_type find_ball (
        ball_data const&_bdat,
        ball_item     *&_same
        )
    {   return this->_bset.find(_bdat, _same);
    }
    __inline_call bool_type find_edge (
        edge_data const&_edat,
        edge_item     *&_same
        )
    {   return this->_eset.find(_edat, _same);
    }
    __inline_call bool_type find_face (
        face_data const&_fdat,
        face_item     *&_same
        )
    {   return this->_fset.find(_fdat, _same);
    }
    __inline_call bool_type find_tria (
        tria_data const&_tdat,
        tria_item     *&_same
        )
    {   return this->_tset.find(_tdat, _same);
    }

    } ;


    }

#   endif   //__RDEL_COMPLEX_3__



