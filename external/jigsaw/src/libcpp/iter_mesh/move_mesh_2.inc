
    /*
    --------------------------------------------------------
     * MOVE-MESH-2: update cell/dual geometries.
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
     * PULL-CONN: cache node-to-cell adjacency lists.
    --------------------------------------------------------
     */

    __static_call
    __normal_call void_type pull_conn (
        mesh_type &_mesh ,
        conn_sets &_conn
        )
    {
        _conn._adj1.set_count( +0 ) ;
        _conn._idx1.set_count(
            _mesh.node().count() + 1,
                containers::tight_alloc , +0 ) ;

        _conn._adj2.set_count( +0 ) ;
        _conn._idx2.set_count(
            _mesh.node().count() + 1,
                containers::tight_alloc , +0 ) ;

        _conn._adj1.set_alloc(
            _mesh.edge().count() * 2) ;
        _conn._adj2.set_alloc(
            _mesh.tri3().count() * 3 +
            _mesh.quad().count() * 4) ;

        iptr_type _npos  = +0 ;
        for (auto _node  = _mesh.node().head() ;
                  _node != _mesh.node().tend() ;
                ++_node, ++_npos)
        {
        if (_node->mark() >= + 0)
        {
    /*-------------------- append adj. lists per node */
            _mesh.connect_1(
            _npos, POINT_tag, _conn._adj1) ;

            _conn._idx1[_npos+1] =
                _conn._adj1.count() ;

            _mesh.connect_2(
            _npos, POINT_tag, _conn._adj2) ;

            _conn._idx2[_npos+1] =
                _conn._adj2.count() ;
        }
        else
        {
    /*-------------------- empty lists for null nodes */
            _conn._idx1[_npos+1] =
                _conn._idx1[ _npos] ;

            _conn._idx2[_npos+1] =
                _conn._idx2[ _npos] ;
        }
        }
    }

    /*
    --------------------------------------------------------
     * MOVE-NODE: "limited" single node coord. update.
    --------------------------------------------------------
     */

    #include "iter_node_2.inc"

    template <
    	typename  node_iter
    >
    __static_call
    __inline_call void_type move_node (
        geom_type &_geom ,
        mesh_type &_mesh ,
        hfun_type &_hfun ,
        real_list &_hval ,
        iter_opts &_opts ,
        node_iter  _node ,
        kern_kind  _kern ,
        iptr_type &_move ,
        conn_list &_conn ,
        real_list &_qold ,
        real_list &_qnew ,
        real_type  _QMIN ,
        real_type  _QLIM ,
        iter_stat &_tcpu

        )
    {
    /*---------------- try variational; fallback on dQ/dx */
        move_kern( _geom, _mesh, _hfun,
            _hval, _opts, _node,
            _kern, _move, _conn,
            _qold, _qnew,
            _QMIN, _QLIM, _tcpu) ;  // variational

        if (_move >= +0 ) return ;

        move_kern( _geom, _mesh, _hfun,
            _hval, _opts, _node,
             dqdx_optimise,
            _move, _conn,
            _qold, _qnew,
            _QMIN, _QLIM, _tcpu) ;  // local dQ/dx

        if (_move >= +0 ) return ;
    }

    template <
        typename  node_iter
             >
    __static_call
    __normal_call void_type move_kern (
        geom_type &_geom ,
        mesh_type &_mesh ,
        hfun_type &_hfun ,
        real_list &_hval ,
        iter_opts &_opts ,
        node_iter  _node ,
        kern_kind  _kern ,
        iptr_type &_move ,
        conn_list &_conn ,
        real_list &_qold ,
        real_list &_qnew ,
        real_type  _QMIN ,
        real_type  _QLIM ,
        iter_stat &_tcpu
        )
    {
    /*---------------- optimise single node's coordinates */
        iptr_type static
        constexpr _ITER = (iptr_type) +5  ;

    #   ifdef  __use_timers
        typename std ::chrono::
        high_resolution_clock::time_point  _ttic ;
        typename std ::chrono::
        high_resolution_clock::time_point  _ttoc ;
        typename std ::chrono::
        high_resolution_clock _time ;

        __unreferenced(_time) ; // why does MSVC need this??
    #   endif//__use_timers

        _move = (iptr_type)-1 ;

        real_type _line[geom_dims] =
            {(real_type)+0.0} ;

        real_type _save[geom_dims] =
            {(real_type)+0.0} ;

        real_type _proj[geom_dims] =
            {(real_type)+0.0} ;

    /*---------------- calc. line search direction vector */

    #   ifdef  __use_timers
        _ttic = _time.now() ;
    #   endif//__use_timers

        real_type _ladj = (real_type) +0. ;

        if (_kern == _odt_optimise)
        {
    /*--------------------------- ODT-style update vector */
            _odt_move_2 (
                _geom, _mesh, _hfun, _hval,
                _conn, _node,
                _line, _ladj) ;
        }
        else
        if (_kern == _cvt_optimise)
        {
    /*--------------------------- CVT-style update vector */
            _cvt_move_2 (
                _geom, _mesh, _hfun, _hval,
                _conn, _node,
                _line, _ladj) ;
        }
        else
        if (_kern == dqdx_optimise)
        {
            if (_QMIN<=_QLIM)
            {
    /*--------------------------- d./dx Q^T update vector */
            dqdx_move_2 (
                _mesh, _conn, _node, _qold,
                _line, _ladj) ;
            }
            else { return ; }
        }

    #   ifdef  __use_timers
        _ttoc = _time.now() ;
        _tcpu._ldir_node += _tcpu.nano_span(_ttic, _ttoc) ;
    #   endif//__use_timers

    /*---------------- scale line search direction vector */
        real_type _xeps =           // delta_x ~= 0.0
       (real_type)+0.01*_opts.qtol() ;

        real_type _xtol =           // delta_x reltol
       +std::sqrt(_opts.qtol()) / +10.0  ;

        if (_kern == dqdx_optimise) // test cost-only
        {
            _QLIM  =
       +std::numeric_limits<real_type>::infinity() ;
        }

        auto _ppos = &_node->pval(0) ;

        real_type _lsqr ;
        _lsqr = std::pow(_ladj, 2) ;
        _xeps = std::pow(_xeps, 2) ;
        _xtol = std::pow(_xtol, 2) ;

        real_type _scal =           // overrelaxation
            (real_type) std::sqrt( 2.0 ) ;

    /*---------------- do backtracking line search iter's */

    #   ifdef  __use_timers
        _ttic = _time.now() ;
    #   endif//__use_timers

        for (auto _idim =
        pred_type::geom_dims; _idim-- != +0; )
        {
            _save[_idim] = _ppos [_idim] ;
        }

        for (auto _iter = +0 ;
                _iter != _ITER; ++_iter )
        {
    /*---------------- push update along search direction */
            for (auto _idim  =
            pred_type::geom_dims; _idim-- != +0; )
            {
                _proj[_idim] =
                    _save[_idim] +
                        _scal* _line[_idim] ;
            }

            pred_type::
            proj_node (_geom, _save, _proj) ;

            for (auto _idim  =
            pred_type::geom_dims; _idim-- != +0; )
            {
                _ppos[_idim] = _proj[_idim] ;
            }

            real_type _XEPS = _xeps * _scal ;
            real_type _XTOL = _xtol * _scal ;

            real_type _lmov =
            pred_type::length_sq(_save, _proj) ;

            if (_lmov <= _XEPS * _lsqr) break;

          //_move  = +1 ; return ;

            _scal *= (real_type)+0.5 ;

    /*---------------- test quasi-monotonicity w.r.t. Q^T */
            _qnew.set_count(0) ;

            loop_cost( _mesh, _conn, _qnew,
                 cell_kind ()) ;

            move_okay( _qnew, _qold, _move,
                _QLIM, _opts.qtol(),
                _lmov, _XTOL* _lsqr) ;

            if (_move >= +0) break ;
        }

    /*---------------- swap with the saved coord. if fail */
        if (_move <= +0)
        {
            for (auto _idim  =
            pred_type::geom_dims; _idim-- != +0; )
            {
                _ppos[_idim] = _save[_idim] ;
            }
        }

    #   ifdef  __use_timers
        _ttoc = _time.now() ;
        _tcpu._lopt_node += _tcpu.nano_span(_ttic, _ttoc) ;
    #   endif//__use_timers

    }

    /*
    --------------------------------------------------------
     * MOVE-DUAL: "limited" single node weight update.
    --------------------------------------------------------
     */

   #include "iter_dual_2.inc"

    template <
        typename  node_iter
             >
    __static_call
    __normal_call void_type move_dual (
        geom_type &_geom ,
        mesh_type &_mesh ,
        hfun_type &_hfun ,
        real_list &_hval ,
        iter_opts &_opts ,
        node_iter  _node ,
        iptr_type &_move ,
        conn_list &_conn ,
        real_list &_dold ,
        real_list &_dnew ,
        real_type  _DMIN ,
        real_type  _DLIM ,
        iter_stat &_tcpu
        )
    {
    /*---------------- optimise single node's coordinates */
        iptr_type static
        constexpr _ITER = (iptr_type) +5  ;

    #   ifdef  __use_timers
        typename std ::chrono::
        high_resolution_clock::time_point  _ttic ;
        typename std ::chrono::
        high_resolution_clock::time_point  _ttoc ;
        typename std ::chrono::
        high_resolution_clock _time ;

        __unreferenced(_time) ; // why does MSVC need this??
    #   endif//__use_timers

        __unreferenced(_geom);
        __unreferenced(_hfun);
        __unreferenced(_hval);

        _move = (iptr_type)-1;

        real_type _wadj, _step, _save;

    /*---------------- calc. line search direction vector */

    #   ifdef  __use_timers
        _ttic = _time.now() ;
    #   endif//__use_timers

        if (_DMIN <= _DLIM)
        {
            dqdw_move_2 (
                _mesh, _conn, _node, _dold,
                _step, _wadj) ;
        }
        else { return ; }

    #   ifdef  __use_timers
        _ttoc = _time.now() ;
        _tcpu._ldir_dual += _tcpu.nano_span(_ttic, _ttoc) ;
    #   endif//__use_timers

    /*---------------- scale line search direction vector */
        real_type _weps =           // delta_w ~= 0.0
            (real_type) .01*_opts.qtol() ;

        _save = _node->pval(
            pred_type::real_dims - 1);

        real_type _scal =           // overrelaxation
            (real_type) std::sqrt( 2.0 ) ;

    /*---------------- do backtracking line search iter's */

    #   ifdef  __use_timers
        _ttic = _time.now() ;
    #   endif//__use_timers

        for (auto _iter = +0 ;
                _iter != _ITER; ++_iter )
        {
            _node->pval(real_dims-1) =
                _save + ( _scal * _step ) ;

            _node->pval(real_dims-1) =
                std::max(-_wadj ,
            _node->pval(real_dims-1));

            _node->pval(real_dims-1) =
                std::min(+_wadj ,
            _node->pval(real_dims-1));

            real_type _wmov =
                std::abs (_save -
            _node->pval(real_dims-1));

            if (_wmov <=
            _weps * _scal * _wadj) break;

            _scal *= (real_type)+0.5 ;

    /*---------------- test quasi-monotonicity w.r.t. Q^D */
            _dnew.set_count(0) ;

            loop_cost( _mesh, _conn, _dnew,
                 dual_kind ()) ;

            move_okay( _dnew, _dold, _move,
                _DLIM, _opts.qtol()) ;

            if (_move >= +0) break ;
        }

    /*---------------- swap with the saved coord. if fail */
        if (_move <= +0)
        {
            _node->pval(real_dims-1) = _save ;
        }

    #   ifdef  __use_timers
        _ttoc = _time.now() ;
        _tcpu._lopt_dual += _tcpu.nano_span(_ttic, _ttoc) ;
    #   endif//__use_timers

    }

    /*
    --------------------------------------------------------
     * SORT-NODE: permutations for node optimisation.
    --------------------------------------------------------
     */

    __static_call
    __normal_call void_type sort_node (
        mesh_type &_mesh ,
        conn_sets &_CONN ,
        iptr_list &_lset ,
        iptr_list &_aset ,
        iptr_list &_nmrk ,
        iptr_list &_amrk ,
        iptr_type  _iout ,
        iptr_type  _isub ,
        real_type  _QLIM ,
        real_type  _DLIM ,
        iter_opts &_opts
        
        )
    {
    #   define PUSHSORT(_NODE)  \
            if (_amrk[_NODE] != _isub)      \
            {               \
                _amrk[_NODE]  = _isub;      \
                _sset.push_tail(            \
                 cost_pair(_NODE, 1.)) ;    \
            }

    #   define PUSHCONN(_NODE)  \
            if (_amrk[_NODE] != _isub)      \
            {               \
                _amrk[_NODE]  = _isub;      \
                _aset.push_tail(_NODE) ;    \
            }

    #   define PUSHCOST(_NODE , _COST)      \
            _qbar[_NODE] += _COST ;         \
            _nadj[_NODE] += +1 ;\
            _qmin[_NODE]  =     \
        std::min (_qmin[_NODE], _COST) ;

        class cost_pair
            {
            public  :
    /*------------------------ tuple for node re-ordering */
            iptr_type           _node ;
            float               _cost ;

    /*------------------------ construct inline from src. */
            __inline_call cost_pair (
                iptr_type const&_nsrc ,
                real_type const&_csrc
                )   :
                   _node (_nsrc),
                   _cost((float)_csrc) {}
            } ;

        class cost_pred
            {
            public  :
    /*------------------------ less-than op. for cost-tup */
            __inline_call
                bool_type operator () (
                cost_pair const&_idat ,
                cost_pair const&_jdat
                ) const
            { return _idat._cost > _jdat._cost ;
            }
            } ;

        typedef
        containers::array<cost_pair> cost_list ;

        real_list _qbar, _qmin ;
        iptr_list _nadj ;
        cost_list _sset ;

        __unreferenced ( _DLIM ) ;
        __unreferenced ( _opts ) ;

        if (_isub == (iptr_type) +0)
        {
    /*-------------------- 1ST SUB-ITER: build full init. */
        _qbar.set_count(
            _mesh.node().count(),
                containers::tight_alloc, +0.0) ;
        _qmin.set_count(
            _mesh.node().count(),
                containers::tight_alloc, +1.0) ;
        _nadj.set_count(
            _mesh.node().count(),
                containers::tight_alloc, + 0 ) ;

        _sset.set_alloc(
            _mesh.node().count())  ;

        pull_conn(_mesh, _CONN) ;

        for (auto _tria  = _mesh.tri3().head() ;
                  _tria != _mesh.tri3().tend() ;
                ++_tria  )
        {
            if (_tria->mark() >= +0)
            {
        /*-------------------- calc. min. scores at nodes */
                iptr_type _inod, _jnod, _knod;
                _inod = _tria->node( 0);
                _jnod = _tria->node( 1);
                _knod = _tria->node( 2);

                real_type _cost;
                _cost = pred_type::tri3_cost (
               &_mesh .node(
                _tria->node(0)).pval(0),
               &_mesh .node(
                _tria->node(1)).pval(0),
               &_mesh .node(
                _tria->node(2)).pval(0),
                typename
                pred_type::cell_kind ()) ;

                PUSHSORT( _inod )
                PUSHCOST( _inod, _cost )
                PUSHSORT( _jnod )
                PUSHCOST( _jnod, _cost )
                PUSHSORT( _knod )
                PUSHCOST( _knod, _cost )
            }
        }

        for (auto _quad  = _mesh.quad().head() ;
                  _quad != _mesh.quad().tend() ;
                ++_quad  )
        {
            if (_quad->mark() >= +0)
            {
        /*-------------------- calc. min. scores at nodes */
                iptr_type _inod, _jnod, _knod,
                          _lnod;
                _inod = _quad->node( 0);
                _jnod = _quad->node( 1);
                _knod = _quad->node( 2);
                _lnod = _quad->node( 3);

                real_type _cost;
                _cost = pred_type::quad_cost (
               &_mesh .node(
                _quad->node(0)).pval(0),
               &_mesh .node(
                _quad->node(1)).pval(0),
               &_mesh .node(
                _quad->node(2)).pval(0),
               &_mesh .node(
                _quad->node(3)).pval(0),
                typename
                pred_type::cell_kind ()) ;

                PUSHSORT( _inod )
                PUSHCOST( _inod, _cost )
                PUSHSORT( _jnod )
                PUSHCOST( _jnod, _cost )
                PUSHSORT( _knod )
                PUSHCOST( _knod, _cost )
                PUSHSORT( _lnod )
                PUSHCOST( _lnod, _cost )
            }
        }

        for (auto _iter  =
            _qbar.count(); _iter-- != +0; )
        {
    /*------------------------ assign score for each node */
            _qbar[_iter] /=
                std::max(+1, _nadj [_iter]) ;
        }

        for (auto _iter  = _sset.head() ;
                  _iter != _sset.tend() ;
                ++_iter  )
        {
            _iter->_cost =
            (float)_qbar [_iter->_node] -
            (float)_qmin [_iter->_node] ;
        }

        algorithms::qsort( _sset.head() ,
                           _sset.tend() ,
            cost_pred () ) ;

        iptr_type _FLAG  = _iout - 2 ; // only "recent"

        for (auto _iter  = _sset.head() ;
                  _iter != _sset.tend() ;
                ++_iter  )
        {
    /*------------------------ push sorted wrt. min.-cost */
            if (std::abs(
            _nmrk[_iter->_node]) >= _FLAG || // recent
            _qmin[_iter->_node]  <= _QLIM )  // skewed
            {
            _amrk[_iter->_node]   = _isub ;
            _aset.push_tail( _iter->_node ) ;
            }
        }

        }
        else
        {
    /*-------------------- NTH sub-iter: init. from prev. */
        for (auto _iter  = _lset.head() ;
                  _iter != _lset.tend() ;
                ++_iter  )
        {
                PUSHCONN( *_iter )
        }

    /*-------------------- add adj.: 1-ring neighbourhood */
        for (auto _iter =
            _aset.count() ; _iter-- != 0; )
        {
             auto _apos =   _aset [_iter] ;

        /*-------------------- push any 1-cell neighbours */
            for (auto _next  =
            _CONN._adj1.head()+_CONN._idx1[_apos+0] ;
                      _next !=
            _CONN._adj1.head()+_CONN._idx1[_apos+1] ;
                    ++_next  )
            {
            if (_next->_kind == EDGE2_tag)
            {
                 auto _eptr =
                _mesh. edge().head()+_next->_cell ;

                PUSHCONN( _eptr->node(0) )
                PUSHCONN( _eptr->node(1) )
            }
            }

        /*-------------------- push any 2-cell neighbours */
            for (auto _next  =
            _CONN._adj2.head()+_CONN._idx2[_apos+0] ;
                      _next !=
            _CONN._adj2.head()+_CONN._idx2[_apos+1] ;
                    ++_next  )
            {
            if (_next->_kind == TRIA3_tag)
            {
                 auto _tptr =
                _mesh. tri3().head()+_next->_cell ;

                PUSHCONN( _tptr->node(0) )
                PUSHCONN( _tptr->node(1) )
                PUSHCONN( _tptr->node(2) )
            }
            else
            if (_next->_kind == QUAD4_tag)
            {
                 auto _qptr =
                _mesh. quad().head()+_next->_cell ;

                PUSHCONN( _qptr->node(0) )
                PUSHCONN( _qptr->node(1) )
                PUSHCONN( _qptr->node(2) )
                PUSHCONN( _qptr->node(3) )
            }
            }
        }

        }
    #   undef   PUSHCOST
    #   undef   PUSHSORT
    #   undef   PUSHCONN
    }

    /*
    --------------------------------------------------------
     * MOVE-NODE: do a single node smoothing pass.
    --------------------------------------------------------
     */

    __static_call
    __normal_call void_type move_node (
        geom_type &_geom ,
        mesh_type &_mesh ,
        conn_sets &_CONN ,
        hfun_type &_hfun ,
        char_type  _kern ,
        real_list &_hval ,
        containers::array< iptr_list> &_nset ,
        iptr_list &_lset ,
        iptr_list &_aset ,
        iptr_list &_amrk ,
        mark_list &_mark ,
        iptr_type  _iout ,
        iptr_type  _isub ,
        iter_opts &_opts ,
        iptr_type &_nmov ,
        real_type  _QLIM ,
        real_type  _DLIM ,
        iter_stat &_tcpu ,
	    std::int32_t    &_rank ,
    	part_sets &_prts
	
        )
    {
    #   define MARK(_NODE) _mark._node[_NODE]

    #   define HEAD(_PASS)(_PASS == +0 ?    \
                           _aset.head() :   \
                           _aset.tail())



    #   define STOP(_PASS)(_PASS == +0 ?    \
                           _aset.tend() :   \
                           _aset.hend())

    #   define ITER(_PASS)(_PASS == +0 ? +1 : -1)
        conn_list _conn;
        real_list _qold, _qnew, _dold, _dnew;

    #   ifdef  __use_timers
        typename std ::chrono::
        high_resolution_clock::time_point  _ttic;
        typename std ::chrono::
        high_resolution_clock::time_point  _ttoc;
        typename std ::chrono::
        high_resolution_clock _time ;

        __unreferenced(_time) ; // why does MSVC need this??
    #   endif//__use_timers

    /*-------------------- permute nodes for optimisation */

    #   ifdef  __use_timers
        _ttic = _time.now() ;
    #   endif//__use_timers

//        _aset.set_count(+0) ;

//        sort_node(_mesh, _CONN, _lset, _aset,
//            _mark._node, _amrk, _iout, _isub,
//            _QLIM,_DLIM, _opts) ;
        
        _nmov = (iptr_type)0;

    #   ifdef  __use_timers
        _ttoc = _time.now() ;
        _tcpu._init_node += _tcpu.time_span(_ttic, _ttoc) ;
    #   endif//__use_timers

    /*-------------------- SYMMETRIC GAUSS-SEIDEL on CELL */

    #   ifdef  __use_timers
        _ttic = _time.now() ;
    #   endif//__use_timers

        _lset.set_count(+0) ;

        if (_opts .tria())  // 1=>GS, 2=>SGS
        {

        auto limit = _prts._lptr[_rank + 1];
        auto start = _prts._lptr[_rank];
         
        if (_rank < 0) {
            limit = _prts._ifls.count();
            start = 0;
        }

        for (auto _pass  = 0; _pass < 2; ++_pass)
            //for (auto _ape = _prts._lptr[_rank]; _ape < _prts._lptr[_rank + 1]; ++ _ape) {
            for (size_t _ape = start; _ape < limit; ++ _ape) {
                auto _apos = _prts._list[_ape];                
                if (_rank < 0)                
                    _apos = _prts._ifls[_ape];
                    
                auto _node = _mesh.node().head() + _apos;
                _conn.set_count( +0) ; // extract set of adj. tri3’s for this node
                _conn.push_tail(
                _CONN._adj2.head()+_CONN._idx2[_apos+0],
                _CONN._adj2.head()+_CONN._idx2[_apos+1]
                     ) ;
                if (_conn.empty()) continue ; // skip any unattached nodes

                if (_mark._node[_apos] >= +0 && (_rank < 0 || _prts._itfc[_apos] == 0)) // skip nodes not allowed to move
                {                             // perhaps also skip interface nodes here too?]
                    _qold.set_count( +0) ;
                    _qnew.set_count( +0) ; // lists of adj. tri3 “scores”

                    // get tri3 scores given current node position
                    real_type _QMIN = loop_cost(_mesh, _conn, _qold, cell_kind());

                    // call kernel to optimise single node position
                    iptr_type _move = -1 ; // haven’t moved yet
                    move_node( _geom, _mesh,
                               _hfun, _hval,
                               _opts, _node, _kern,
                               _move, _conn,
                               _qold, _qnew,
                               _QMIN, _QLIM, _tcpu) ;

                    if (_move > +0)  // if node has been successfully optimised
                    {   if (_rank < 0)
                            std::cout << "still got in here...\n";
                        _hval[_apos] = (real_type)-1; // to force a recalc. of internal data

                        if (std::abs(MARK( _apos )) !=_iout) // keep track of moving nodes
                        {
                            if (MARK( _apos ) >= 0)
                                MARK( _apos ) = +_iout;
                            else
                                MARK( _apos ) = -_iout;
                            _nset[_rank >= 0 ? _rank : 0].push_tail (_apos) ; // array of nodes that have moved
                        }
                        _nmov += +1 ;
                    }
                }
            } 
            }
            
            // here


//        for (auto _pass = 0; _pass < 2; ++ _pass)
//        for (auto _apos  = HEAD(_pass) ;
//                  _apos != STOP(_pass) ;
//                  _apos += ITER(_pass) )
//        {
//             //std::cout << *_apos << std::endl;
//             auto _node  =
//            _mesh.node().head()+ *_apos ;
//
//        /*---------------- assemble a local tria. stencil */
//            _conn.set_count( +0) ;
//            _conn.push_tail(
//            _CONN._adj2.head()+_CONN._idx2[*_apos+0],
//            _CONN._adj2.head()+_CONN._idx2[*_apos+1]
//                ) ;
//
//            if (_conn.empty()) continue ;
//
//            if (_mark._node[*_apos] >= +0)
//            {
//        /*---------------- attempt to optimise CELL geom. */
//            _qold.set_count( +0) ;
//            _qnew.set_count( +0) ;
//
//            real_type  _QMIN =
//            loop_cost( _mesh,
//                _conn, _qold, cell_kind());
//
//            iptr_type _move = -1 ;
//
//            if (_move < +0 )
//            {
//        /*---------------- do optimisation of node coord. */
//                move_node( _geom, _mesh,
//                    _hfun, _hval,
//                    _opts, _node, _kern,
//                    _move, _conn,
//                    _qold, _qnew,
//                    _QMIN, _QLIM, _tcpu) ;
//            }
//
//            if (_move > +0 )
//            {
//        /*---------------- update when state is improving */
//            _hval[*_apos] = (real_type)-1;
//
//            if (std::abs(
//                MARK( *_apos )) !=_iout)
//            {
//                if (MARK( *_apos ) >= 0)
//                MARK( *_apos ) = +_iout;
//                else
//                MARK( *_apos ) = -_iout;
//
//                _nset[0].push_tail (*_apos) ;
//            }
//
//            _lset.push_tail (*_apos) ;
//
//            _nmov += +1 ;
//            }
//            }
//        }
//        }

    #   ifdef  __use_timers
        _ttoc = _time.now() ;
        _tcpu._core_node += _tcpu.time_span(_ttic, _ttoc) ;
    #   endif//__use_timers

    #   undef   MARK
    #   undef   HEAD
    #   undef   STOP
    #   undef   ITER
    }

    /*
    --------------------------------------------------------
     * MOVE-DUAL: do a single dual smoothing pass.
    --------------------------------------------------------
     */

    __static_call
    __normal_call void_type move_dual (
        geom_type &_geom ,
        mesh_type &_mesh ,
        conn_sets &_CONN ,
        hfun_type &_hfun ,
        real_list &_hval ,
        iptr_list &_nset ,
        iptr_list &_lset ,
        iptr_list &_aset ,
        iptr_list &_amrk ,
        mark_list &_mark ,
        iptr_type  _iout ,
        iptr_type  _isub ,
        iter_opts &_opts ,
        iptr_type &_nmov ,
        real_type  _QLIM ,
        real_type  _DLIM ,
        iter_stat &_tcpu
        )
    {
    #   define MARK(_NODE) _mark._node[_NODE]

    #   define HEAD(_PASS)(_PASS == +0 ?    \
                           _aset.head() :   \
                           _aset.tail())

    #   define STOP(_PASS)(_PASS == +0 ?    \
                           _aset.tend() :   \
                           _aset.hend())

    #   define ITER(_PASS)(_PASS == +0 ? +1 : -1)

        conn_list _conn;
        real_list _qold, _qnew, _dold, _dnew;

    #   ifdef  __use_timers
        typename std ::chrono::
        high_resolution_clock::time_point  _ttic ;
        typename std ::chrono::
        high_resolution_clock::time_point  _ttoc ;
        typename std ::chrono::
        high_resolution_clock _time ;

        __unreferenced(_time) ; // why does MSVC need this??
    #   endif//__use_timers

    /*-------------------- permute nodes for optimisation */

    #   ifdef  __use_timers
        _ttic = _time.now() ;
    #   endif//__use_timers

        _aset.set_count(+0) ;

        sort_node(_mesh, _CONN, _lset, _aset,
            _mark._node, _amrk, _iout, _isub,
            _QLIM,_DLIM, _opts) ;

        _nmov = (iptr_type)0;

    #   ifdef  __use_timers
        _ttoc = _time.now() ;
        _tcpu._init_dual += _tcpu.time_span(_ttic, _ttoc) ;
    #   endif//__use_timers

    /*-------------------- SYMMETRIC GAUSS-SEIDEL on DUAL */

    #   ifdef  __use_timers
        _ttic = _time.now() ;
    #   endif//__use_timers

        _lset.set_count(+0) ;

        if (_opts .dual())  // 1=>GS, 2=>SGS
        {
        for (auto _pass  = 0; _pass < 2; ++_pass)
        for (auto _apos  = HEAD(_pass) ;
                  _apos != STOP(_pass) ;
                  _apos += ITER(_pass) )
        {
             auto _node  =
            _mesh.node().head()+ *_apos ;

        /*---------------- assemble a local tria. stencil */
            _conn.set_count( +0) ;
            _conn.push_tail(
            _CONN._adj2.head()+_CONN._idx2[*_apos+0],
            _CONN._adj2.head()+_CONN._idx2[*_apos+1]
                ) ;

            if (_conn.empty()) continue ;

        /*---------------- attempt to optimise DUAL geom. */
            _dold.set_count( +0) ;
            _dnew.set_count( +0) ;

            real_type  _DMIN =
            loop_cost( _mesh,
                _conn, _dold, dual_kind());

            iptr_type _move = -1 ;

            if (_move < +0 )
            {
        /*---------------- do optimisation of node weight */
                move_dual( _geom, _mesh,
                    _hfun, _hval,
                    _opts, _node,
                    _move, _conn,
                    _dold, _dnew,
                    _DMIN, _DLIM, _tcpu) ;
            }

            if (_move > +0 )
            {
        /*---------------- update when state is improving */
            if (std::abs(
                MARK( *_apos )) !=_iout)
            {
                if (MARK( *_apos ) >= 0)
                MARK( *_apos ) = +_iout;
                else
                MARK( *_apos ) = -_iout;

                _nset.push_tail (*_apos) ;
            }

            _lset.push_tail(*_apos) ;

            _nmov += +1 ;
            }
        }
        }

    #   ifdef  __use_timers
        _ttoc = _time.now() ;
        _tcpu._core_dual += _tcpu.time_span(_ttic, _ttoc) ;
    #   endif//__use_timers

    #   undef   MARK
    #   undef   HEAD
    #   undef   STOP
    #   undef   ITER
    }



