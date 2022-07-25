
    /*
    --------------------------------------------------------
     * ITER-MESH-2: mesh-optimisation for 2-complexes.
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

#   pragma once

#include <numeric>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <pthread.h>
#   ifndef __ITER_MESH_2__
#   define __ITER_MESH_2__

    namespace  mesh {

    /*
    --------------------------------------------------------
     * ITER-MESH-2: optimise mixed 2-complex meshes
    --------------------------------------------------------
     */

    template <
    typename G ,
    typename M ,
    typename H ,
    typename P
             >
    class iter_mesh_2
    {
    public  :
    typedef  M                          mesh_type ;
    typedef  G                          geom_type ;
    typedef  H                          hfun_type ;
    typedef  P                          pred_type ;

    typedef typename
            mesh_type::real_type        real_type ;
    typedef typename
            mesh_type::iptr_type        iptr_type ;

    iptr_type static constexpr min_subit = +2 ;
    iptr_type static constexpr max_subit = +8 ;

    iptr_type static constexpr
            topo_dims =      pred_type::topo_dims ;
    iptr_type static constexpr
            geom_dims =      pred_type::geom_dims ;
    iptr_type static constexpr
            real_dims =      pred_type::real_dims ;

    typedef char_type                   kern_kind ;

    char_type static                // optm. kern. selector
        constexpr _odt_optimise = +1 ;
    char_type static
        constexpr _cvt_optimise = +2 ;
    char_type static
        constexpr _h95_optimise = +3 ;
    char_type static
        constexpr dqdx_optimise = +5 ;

    typedef char_type                   flip_kind ;

    flip_kind static                // optm. kern. selector
        constexpr laguerre_flip = +1 ;
    flip_kind static
        constexpr delaunay_flip = +2 ;
    flip_kind static
        constexpr topology_flip = +3 ;

    class   cell_kind{} ;           // dummies for overload
    class   dual_kind{} ;

    typedef mesh::iter_params  <
            real_type ,
            iptr_type          >        iter_opts ;

    typedef mesh::iter_timers  <
            real_type ,
            iptr_type          >        iter_stat ;

    typedef containers
            ::array< iptr_type >        iptr_list ;
    typedef containers
            ::array< size_t    >        uint_list ;
    typedef containers
            ::array< real_type >        real_list ;
    typedef containers
            ::array< bool      >        bool_list ;
    typedef containers
            ::array< std::int32_t >     sint_list ;

    class mark_list                 // integer cell markers
        {
        public  :
        iptr_list                      _node;
        iptr_list                      _edge;
        iptr_list                      _tri3;
        iptr_list                      _quad;
        } ;

    class part_sets                 // mesh parallel decomp.
        {
        public  :
        uint_list                      _lptr;
        iptr_list                      _list;
        iptr_list                      _part;
        bool_list                      _itfc; 
        iptr_list                      _ifls;
        iptr_list                      _trls;
        iptr_list                      _seqs;
        } ;

    typedef typename
        mesh_type::connector            conn_list ;

    class conn_sets                 // cache neighbourhoods
        {
        public  :
        conn_list                      _adj1;
        uint_list                      _idx1;
        conn_list                      _adj2;
        uint_list                      _idx2;
        } ;

    public  :

    /*
    --------------------------------------------------------
     * FLIP-SIGN: flip cells for +ve iter. cost fn.
    --------------------------------------------------------
     */

    #include "_bfs_mesh_2.inc"


    /*
    --------------------------------------------------------
     * COST-MESH: 1-neighbourhood cost vector util.
    --------------------------------------------------------
     */

    #include "cost_mesh_2.inc"


    /*
    --------------------------------------------------------
     * PART-MESH: paritions for parallel decomposition.
    --------------------------------------------------------
     */

    #include "part_mesh_2.inc"


    /*
    --------------------------------------------------------
     * MOVE-MESH: do single cell/dual smoothing passes.
    --------------------------------------------------------
     */

    #include "move_mesh_2.inc"


    /*
    --------------------------------------------------------
     * FLIP-MESH: "flip" mesh topology until Delaunay.
    --------------------------------------------------------
     */

    #include "flip_mesh_2.inc"

    
    /*
    --------------------------------------------------------
     * _ZIP-MESH: merge/split operations on cells.
    --------------------------------------------------------
     */

    #include "_zip_mesh_2.inc"
    

    /*------------------------------ helper: init. marker */

    __static_call
    __normal_call void_type init_mark (
        mesh_type &_mesh ,
        mark_list &_mark ,
        iptr_type  _flag = +0
        )
    {
        iptr_type _nnN1 = std::max(
           (iptr_type) _mark. _node.count() ,
           (iptr_type) _mesh.node().count()
                ) ;
        iptr_type _nnE2 = std::max(
           (iptr_type) _mark. _edge.count() ,
           (iptr_type) _mesh.edge().count()
                ) ;
        iptr_type _nnT3 = std::max(
           (iptr_type) _mark. _tri3.count() ,
           (iptr_type) _mesh.tri3().count()
                ) ;
        iptr_type _nnQ4 = std::max(
           (iptr_type) _mark. _quad.count() ,
           (iptr_type) _mesh.quad().count()
                ) ;

        _mark._node.set_count(_nnN1,
            containers::loose_alloc, _flag) ;

        _mark._edge.set_count(_nnE2,
            containers::loose_alloc, _flag) ;

        _mark._tri3.set_count(_nnT3,
            containers::loose_alloc, _flag) ;

        _mark._quad.set_count(_nnQ4,
            containers::loose_alloc, _flag) ;
    }

    /*------------------------------ helper: init. bounds */

    __static_call
    __normal_call void_type init_bnds (
        mesh_type &_mesh ,
        mark_list &_mark
        )
    {
    /*------------------------------ mark bnd. item <= -1 */
        conn_list _conn ;
        iptr_type _nnN1  = +0 ;
        for (auto _node  = _mesh.node().head() ;
                  _node != _mesh.node().tend() ;
                ++_node, ++_nnN1 )
        {
            if (_node->mark() >= +0)
            {
            if (_node->feat()
                    != mesh::null_feat)
            {
                _mark._node[_nnN1]  = -1 ;
            }
            }
        }

        iptr_type _nnE2  = +0 ;
        for (auto _edge  = _mesh.edge().head() ;
                  _edge != _mesh.edge().tend() ;
                ++_edge, ++_nnE2 )
        {
            if (_edge->mark() >= +0)
            {
            if (_edge->self() >= +1)
            {
                _mark._node[
                    _edge->node(0)] = -1 ;
                _mark._node[
                    _edge->node(1)] = -1 ;
            }
            else
            {
                _conn.set_count(0) ;

                _mesh.connect_2(
            &_edge->node(0), EDGE2_tag, _conn) ;

                if (_conn.count () != +2)
                {
                _mark._node[
                    _edge->node(0)] = -1 ;
                _mark._node[
                    _edge->node(1)] = -1 ;
                }
            }
            }
        }
    }

    /*------------------------------ helper: init. scores */

    __static_call
    __normal_call real_type init_cost (
        mesh_type &_mesh,
        iter_opts &_opts
        )
    {
        real_type _QMIN = (real_type) +1.;

        for (auto _cell  = _mesh.tri3().head() ;
                  _cell != _mesh.tri3().tend() ;
                ++_cell  )
        {
            if (_cell->mark() >= +0 )
            {
        /*--------------------- test initial cell quality */
            real_type _cost;
            _cost = pred_type::tri3_cost  (
               &_mesh .node(
                _cell->node(0)).pval(0),
               &_mesh .node(
                _cell->node(1)).pval(0),
               &_mesh .node(
                _cell->node(2)).pval(0),
                typename
                pred_type::cell_kind ())  ;

            _QMIN = std::min (_QMIN, _cost) ;
            _QMIN = std::max (_QMIN,
                              _opts.qlim()) ;
            }
        }

        for (auto _cell  = _mesh.quad().head() ;
                  _cell != _mesh.quad().tend() ;
                ++_cell  )
        {
            if (_cell->mark() >= +0 )
            {
        /*--------------------- test initial cell quality */
            real_type _cost;
            _cost = pred_type::quad_cost  (
               &_mesh .node(
                _cell->node(0)).pval(0),
               &_mesh .node(
                _cell->node(1)).pval(0),
               &_mesh .node(
                _cell->node(2)).pval(0),
               &_mesh .node(
                _cell->node(3)).pval(0),
                typename
                pred_type::cell_kind ())  ;

            _QMIN = std::min (_QMIN, _cost) ;
            _QMIN = std::max (_QMIN,
                              _opts.qlim()) ;
            }
        }

        return _QMIN ;
    }

    /*
    --------------------------------------------------------
     * ITER-MESH: "hill-climbing" type mesh optimisation.
    --------------------------------------------------------
     */

    template <
        typename  text_dump
             >
    __static_call
    __normal_call void_type iter_mesh (
        geom_type &_geom ,
        hfun_type &_hfun ,
        mesh_type &_mesh ,
        kern_kind  _kern ,
        iter_opts &_opts ,
        text_dump &_dump
        )
    {
	
    
    /*------------------------------ push log-file header */
        if (_opts.verb() >= 0 )
        {
            _dump.push(
    "#------------------------------------------------------------\n"
    "#    |MOVE.|      |FLIP.|      |MERGE|      |SPLIT| \n"
    "#------------------------------------------------------------\n"
                    ) ;
        }
        auto num_threads = _opts.threads();
        iter_stat  _tcpu ;
//        if (num_threads > 1)
        BS::thread_pool pool(num_threads);
    #   ifdef  __use_timers
        typename std ::chrono::
        high_resolution_clock::time_point  _ttic ;
        typename std ::chrono::
        high_resolution_clock::time_point  _ttoc ;
        typename std ::chrono::
        high_resolution_clock _time ;

        __unreferenced(_time) ; // why does MSVC need this??
    #   endif//__use_timers

    /*------------------------------ ensure deterministic */
        std::srand( +1 ) ;

    /*------------------------------ push boundary marker */
	    std::ofstream out;
        mark_list _mark ;
        containers::array< iptr_list >        multi_nset;
        init_mark(_mesh, _mark) ;
        init_bnds(_mesh, _mark) ;        

        flip_sign(_mesh);

    /*------------------------------ do optimisation loop */
        bool_type
        static constexpr ITER_FLIP = true;

        iptr_type
        static constexpr ITER_MIN_ = min_subit ;
        iptr_type
        static constexpr ITER_MAX_ = max_subit ;

        real_type _QMIN = init_cost (_mesh, _opts) ;
	
        for (auto _iter = +1 ;
            _iter <= _opts.iter(); ++_iter)
        {
            std::cout << "in opti iter " << _iter << '\n';
    /*------------------------------ set-up current iter. */
            init_mark(_mesh, _mark,
                std::max(_iter-1, +0)) ;

            real_list _hval;
            _hval.set_count(
                _mesh. node().count(),
            containers::tight_alloc, (real_type) -1.0) ;
            containers::array< iptr_type > multi_nmov;
            multi_nmov.set_count(num_threads, containers::tight_alloc);
//            iptr_type _nmov = +0 ;
            iptr_type _nflp = +0 ;
            iptr_type _nzip = +0 ;
            iptr_type _ndiv = +0 ;
            for (auto i = 0; i < num_threads; ++i)
                multi_nmov[i] = +0;
            auto & _nmov = multi_nmov[0]; // alias to first of multi_nmov

    /*------------------------------ scale quality thresh */
            iptr_type _nsub = _iter +0 ;

            _nsub =
            std::min(ITER_MAX_, _nsub) ;
            _nsub =
            std::max(ITER_MIN_, _nsub) ;

            real_type _DLIM =
           (real_type)+1.-_opts.qtol() ;

            real_type _QLIM =
           (real_type)+.750 * _QMIN +
           (real_type)+.075 * _iter ;

            _QLIM = std::min(
                _opts.qlim () , _QLIM) ;

    /*------------------------------ 1. CELL GEOM. PASSES */

            if (_opts.tria())
            {
    /*------------------------------ update mesh geometry */
    #       ifdef  __use_timers
            _ttic = _time.now() ;
    #       endif//__use_timers

            // hard code in a lookup table for affinity on cori-haswell
            // Couldn't figure out how to use containers::hash_table
            // and couldn't figure out how to get unordered map to work with
            // iptr_type/iptr_list.

            const std::unordered_map<int32_t, std::vector<int32_t> > affinity_lookup = {
                    {1, {0}},
                    {2, {0, 16}},
                    {4, {0, 1, 16, 17}},
                    {8, {0, 1, 2, 3, 16, 17, 18, 19}},
                    {16, {0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23}},
                    {32, {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31}},
                    {64, {0, 32, 1, 33, 2, 34, 3, 35, 4, 36, 5, 37, 6, 38, 7, 39, 8, 40, 9, 41, 10, 42, 11, 43, 12, 44, 13, 45, 14, 46, 15, 47,
                          16, 48, 17, 49, 18, 50, 19, 51, 20, 52, 21, 53, 22, 54, 23, 55, 24, 56, 25, 57, 26, 58, 27, 59, 28, 60, 29, 61, 30, 62, 31, 63}}
            };

            conn_sets _conn ;
            pull_conn(_mesh, _conn);

            iptr_list whole_aset, whole_lset, _amrk, _amrk2;
            whole_aset.set_alloc(_mesh.node().count());
            whole_lset.set_alloc(_mesh.node().count());


            _amrk.set_count(_mesh.node().count(), containers::tight_alloc, -1);
            _amrk2.set_count(_mesh.node().count(), containers::tight_alloc, -1);

            sort_node(_mesh, _conn, whole_lset, whole_aset,
                    _mark._node, _amrk2, _iter, 0,
                    _QLIM,_DLIM, _opts);

            part_sets _part;
            part_mesh(_mesh, _part, num_threads, whole_aset) ;

            containers::array< iptr_list > multi_aset;
            containers::array< iptr_list > multi_lset;


            multi_aset.set_count(num_threads, containers::tight_alloc);
            multi_lset.set_count(num_threads, containers::tight_alloc);
            multi_nset.set_count(num_threads);

            for (auto i = 0; i < num_threads; ++i) {
                auto j = _part._lptr[i + 1] - _part._lptr[i];
                multi_lset[i].set_alloc(j);
                multi_aset[i].set_alloc(j);
                multi_nset[i].set_count(+0);
            }

            auto affinity = [] (auto rank) {
                cpu_set_t set;
                CPU_ZERO(&set);
                CPU_SET(rank, &set);
                pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &set);
            };

            auto interface = [&](auto rank, auto pass_min, auto pass_max) {
                auto r = rank == std::numeric_limits<iptr_type>::min() + 1 ?
                         0 : -1 - rank;

                affinity(affinity_lookup.at(num_threads)[r]);

                for (auto _isub = + 0; _isub != _nsub; ++_isub ) {
                    if (_opts.verb() >= -+3)
                        _dump.push("**CALL MOVE-NODE...\n");
                    iptr_type _nloc;
                    move_node(_geom, _mesh, _conn,
                              _hfun, _kern, _hval,
                              multi_nset[r], multi_lset[r], multi_aset[r],
                              _amrk, _mark,
                              _iter, _isub, _opts,
                              _nloc, _QLIM, _DLIM, _tcpu,
                              rank, _part,
                              pass_min, pass_max);
                    _nloc = _nloc / 2;
                    multi_nmov[r] = std::max(multi_nmov[r], _nloc);
                }

            };

	        auto task = [&](auto rank) {

                auto start = std::chrono::high_resolution_clock::now();

                affinity(affinity_lookup.at(num_threads)[rank]);

                for (auto _isub = + 0; _isub != _nsub; ++_isub ) {
                    if (_opts.verb() >= +3)
                        _dump.push("**CALL MOVE-NODE...\n");



                    iptr_type _nloc;
                    move_node(_geom, _mesh, _conn,
                              _hfun, _kern, _hval,
                              multi_nset[rank], multi_lset[rank], multi_aset[rank],
                              _amrk, _mark,
                              _iter, _isub, _opts,
                              _nloc, _QLIM, _DLIM, _tcpu, rank, _part, 0, 2);

                    _nloc = _nloc / 2;
                    multi_nmov[rank] = std::max(multi_nmov[rank], _nloc);
                }

                auto end = std::chrono::high_resolution_clock::now();

                {
                    std::string str = "./thread_time/";
                    str.append(std::to_string(num_threads).append("/"));
                    std::filesystem::create_directories(str);
                    str.append(std::to_string(rank).append(".csv"));
                    std::ofstream out;
                    out.open(str, std::ios_base::app);
                    out << std::chrono::duration_cast
                            <std::chrono::milliseconds>(end - start).count()
                        << '\n';
                    out.close();
                }

	        };


            if (num_threads > 1) {
                for (auto r = 0; r < num_threads; ++r)
                    if (_part._seqs[r] == 1)
                        pool.push_task(interface, -1 - r, 0, 1);
                pool.wait_for_tasks();

                interface(std::numeric_limits<iptr_type>::min() + 1, 0, 1);

                for (auto r = 0; r < num_threads; ++r)
                    pool.push_task(task, r);
                pool.wait_for_tasks();

                for (auto r = 0; r < num_threads; ++r)
                    if (_part._seqs[r] == 1)
                        pool.push_task(interface, -1 - r, 1, 2);
                pool.wait_for_tasks();

                interface(std::numeric_limits<iptr_type>::min() + 1, 1, 2);

                auto reduction_task = [&](auto r, auto c) {
                    if (multi_nset[r + (c / 2)].count() > +0)
                        for (auto it = multi_nset[r + (c / 2)].head(); it != multi_nset[r + (c / 2)].tend(); ++it)
                            multi_nset[r].push_tail(*it);
                };


                if (num_threads > 2) {

                    auto s = 0;
                    for (auto i = 1; i < num_threads; ++i)
                        s += multi_nset[i].count();

                    if (s > 0)
                        for (auto cycle = 2; cycle < num_threads; cycle *= 2) {
                            for (auto rank = 0; rank < num_threads; rank += cycle)
                                pool.push_task(reduction_task, rank, cycle);
                            pool.wait_for_tasks();
                        }
                }

                for (auto i = 1; i < num_threads; ++i)
                    _nmov += multi_nmov[i];

                if (multi_nset[num_threads / 2].count() > 0)
                    for (auto it = multi_nset[num_threads / 2].head();
                         it != multi_nset[num_threads / 2].tend(); ++it)
                        multi_nset[0].push_tail(*it);

            } else
                task(0);

    #       ifdef  __use_timers
            _ttoc = _time.now() ;
            _tcpu._move_node +=
                  _tcpu.time_span(_ttic , _ttoc);
    #       endif//__use_timers

    /*------------------------------ update mesh topology */
    #       ifdef  __use_timers
            _ttic = _time.now() ;
    #       endif//__use_timers

            if (ITER_FLIP)
            {
                if (_opts.verb() >= +3)
                    _dump.push(
                "**CALL FLIP-MESH...\n" ) ;

                iptr_type  _nloc;
                flip_mesh( _geom, _mesh , _hfun ,
                    _conn, multi_nset[0], _mark ,
                +3 * _iter - 2  , _nloc ) ;

                _nflp +=   _nloc;

            }

    #       ifdef  __use_timers
            _ttoc = _time.now() ;
            _tcpu._topo_flip +=
                  _tcpu.time_span(_ttic , _ttoc);
    #       endif//__use_timers
            }

    /*------------------------------ 2. DUAL GEOM. PASSES */

            if (_opts.dual())
            {
    /*------------------------------ update mesh geometry */
    #       ifdef  __use_timers
            _ttic = _time.now() ;
    #       endif//__use_timers

             part_sets _part;
             part_mesh(_mesh, _part, num_threads) ;

             iptr_list _amrk;
             containers::array< iptr_list > multi_aset;
             containers::array< iptr_list > multi_lset;

             // Possibly global -- _amrk
             _amrk.set_count(_mesh.node().count(), containers::tight_alloc, -1);
             multi_aset.set_count(num_threads, containers::tight_alloc);
             multi_lset.set_count(num_threads, containers::tight_alloc);
             multi_nset.set_count(num_threads);

             for (auto i = 0; i < num_threads; ++i) {
                 auto j = _part._lptr[i + 1] - _part._lptr[i];
                 multi_lset[i].set_alloc(j);
                 multi_aset[i].set_alloc(j);
                 multi_nset[i].set_count(+0);
             }
             _nsub = std::max(_nsub/2, 1);
             conn_sets _conn ;

             pull_conn(_mesh, _conn);

             auto interface = [&](auto rank, auto pass_min, auto pass_max) {
                 auto r = rank == std::numeric_limits<iptr_type>::min() + 1 ?
                          0 : -1 - rank;
                 for (auto _isub = + 0; _isub != _nsub; ++_isub ) {
                     if (_opts.verb() >= +3)
                         _dump.push("**CALL MOVE-DUAL...\n");
                     iptr_type _nloc;

                     move_dual( _geom, _mesh , _conn ,
                                _hfun, _hval,
                                multi_nset[r], multi_lset[r], multi_aset[r],
                                _amrk, _mark,
                                _iter, _isub, _opts ,
                                _nloc, _QLIM, _DLIM ,
                                _tcpu, rank,
                                _part, pass_min,
                                pass_max);
                     _nloc = _nloc / 2;
                     _nmov = std::max(multi_nmov[r], _nloc);
                 }
             };

             auto task = [&](auto rank) {
                 for (auto _isub = + 0; _isub != _nsub; ++_isub ) {
                     if (_opts.verb() >= +3)
                         _dump.push("**CALL MOVE-DUAL...\n");
                     iptr_type _nloc;

                     move_dual( _geom, _mesh , _conn ,
                                _hfun, _hval,
                                multi_nset[rank], multi_lset[rank], multi_aset[rank],
                                _amrk, _mark,
                                _iter, _isub, _opts ,
                                _nloc, _QLIM, _DLIM ,
                                _tcpu, rank, _part, 0, 2);

                     _nloc = _nloc / 2;
                     multi_nmov[rank] = std::max(multi_nmov[rank], _nloc);
                 }
             };

             if (num_threads > 1) {

                 for (auto r = 0; r < num_threads; ++r)
                     if (_part._seqs[r] == 1)
                         pool.push_task(interface, -1 - r, 0, 1);
                 pool.wait_for_tasks();

                 interface(std::numeric_limits<iptr_type>::min() + 1, 0, 1);

                 for (auto r = 0; r < num_threads; ++r)
                     pool.push_task(task, r);
                 pool.wait_for_tasks();

                 for (auto r = 0; r < num_threads; ++r)
                     if (_part._seqs[r] == 1)
                         pool.push_task(interface, -1 - r, 1, 2);
                 pool.wait_for_tasks();

                 interface(std::numeric_limits<iptr_type>::min() + 1, 1, 2);

                 auto reduction_task = [&](auto r, auto c) {
                     if (multi_nset[r + (c / 2)].count() > +0)
                         for (auto it = multi_nset[r + (c / 2)].head(); it != multi_nset[r + (c / 2)].tend(); ++it)
                             multi_nset[r].push_tail(*it);
                 };

                 if (num_threads > 2) {
                     auto s = 0;
                     for (auto i = 1; i < num_threads; ++i)
                         s += multi_nset[i].count();

                     if (s > 0)
                         for (auto cycle = 2; cycle < num_threads; cycle *= 2) {
                             for (auto rank = 0; rank < num_threads; rank += cycle)
                                 pool.push_task(reduction_task, rank, cycle);
                             pool.wait_for_tasks();
                         }
                 }

                 for (auto i = 1; i < num_threads; ++i)
                     _nmov += multi_nmov[i];
                 if (multi_nset[num_threads / 2].count() > 0)
                     for (auto it = multi_nset[num_threads / 2].head();
                          it != multi_nset[num_threads / 2].tend(); ++it)
                         multi_nset[0].push_tail(*it);

             } else
                 task(0);



            _tcpu._move_dual +=
                  _tcpu.time_span(_ttic , _ttoc);
    #       endif//__use_timers

    /*------------------------------ update mesh topology */
    #       ifdef  __use_timers
            _ttic = _time.now() ;
    #       endif//__use_timers

            if (ITER_FLIP)
            {
                if (_opts.verb() >= +3)
                    _dump.push(
                "**CALL FLIP-MESH...\n" ) ;

                iptr_type  _nloc;
                flip_mesh( _geom, _mesh , _hfun ,
                    _conn, multi_nset[0], _mark ,
                +3 * _iter - 1  , _nloc ) ;

                _nflp +=   _nloc;
            }

    #       ifdef  __use_timers
            _ttoc = _time.now() ;
            _tcpu._topo_flip +=
                  _tcpu.time_span(_ttic , _ttoc);
    #       endif//__use_timers

            }

    /*------------------------------ 3. ZIP + DIV SUBFACE */

            if (_iter < _opts.iter())
            {
    /*------------------------------ change mesh topology */
    #       ifdef  __use_timers
            _ttic = _time.now() ;
    #       endif//__use_timers

            multi_nset[0].set_count(+0) ;    // don't flip twice!

            if (_opts.zip_ () ||
                _opts.div_ () )
            {
                if (_opts.verb() >= +3)
                    _dump.push(
                "**CALL _ZIP-MESH...\n" ) ;

                _zip_mesh( _geom, _mesh , _hfun ,
                    _kern, _hval, multi_nset[0] ,
                    _mark, _iter, _opts ,
                    _QLIM, _DLIM,
                    _nzip, _ndiv, _tcpu ) ;
            }

    #       ifdef  __use_timers
            _ttoc = _time.now() ;
            _tcpu._topo_zips +=
                  _tcpu.time_span(_ttic , _ttoc);
    #       endif//__use_timers

    /*------------------------------ update mesh topology */

    #       ifdef  __use_timers
            _ttic = _time.now() ;
    #       endif//__use_timers

            if (ITER_FLIP)
            {
                if (_opts.verb() >= +3)
                    _dump.push(
                "**CALL FLIP-MESH...\n" ) ;

                iptr_type  _nloc;
                flip_mesh( _geom, _mesh , _hfun ,
                    multi_nset[0], _mark,
                +3 * _iter - 0  , _nloc ) ;

                _nflp +=   _nloc;
            }

    #       ifdef  __use_timers
            _ttoc = _time.now() ;
            _tcpu._topo_flip +=
                  _tcpu.time_span(_ttic , _ttoc);
    #       endif//__use_timers

            } // if (_iter < _opts.iter())

    /*------------------------------ dump optim. progress */
            if (_opts.verb() >= 0)
            {
            std::stringstream _sstr ;
            _sstr << std::setw(11) << _nmov
                  << std::setw(13) << _nflp
                  << std::setw(13) << _nzip
                  << std::setw(13) << _ndiv
                  <<   "\n" ;
            _dump.push(_sstr.str()) ;
            }

    /*------------------------------ has iter. converged? */
        //  if (_nset.count() == 0) break ;
            if (_nmov == +0 &&
                _nzip == +0 &&
                _ndiv == +0 &&
                _nflp == +0 )       break ;
        }

	{
		out.open("./time_results.csv", std::ios_base::app);
		out << std::scientific
		    << std::setprecision(2)	
		    << _tcpu._move_node
		    << '\t'
		    << _tcpu._topo_flip
		    << '\t'
		    << _tcpu._topo_zips
            << '\t';
	}
	

        if (_opts.verb() >= +2)
        {
    /*------------------------------ print method metrics */
            _dump.push("\n");
            _dump.push("**TIMING statistics...\n") ;

            _dump.push("  MOVE-NODE: ");
            _dump.push(
            std::to_string(_tcpu._move_node)) ;
            _dump.push("\n");
            _dump.push(" *init-node: ");
            _dump.push(
            std::to_string(_tcpu._init_node)) ;
            _dump.push("\n");
            _dump.push(" *core-node: ");
            _dump.push(
            std::to_string(_tcpu._core_node)) ;
            _dump.push("\n");
            _dump.push(" *xDIR-node: ");
            _dump.push(
            std::to_string(_tcpu._ldir_node)) ;
            _dump.push("\n");
            _dump.push(" *xOPT-node: ");
            _dump.push(
            std::to_string(_tcpu._lopt_node)) ;
            _dump.push("\n\n");

            _dump.push("  MOVE-DUAL: ");
            _dump.push(
            std::to_string(_tcpu._move_dual)) ;
            _dump.push("\n");
            _dump.push(" *init-dual: ");
            _dump.push(
            std::to_string(_tcpu._init_dual)) ;
            _dump.push("\n");
            _dump.push(" *core-dual: ");
            _dump.push(
            std::to_string(_tcpu._core_dual)) ;
            _dump.push("\n");
            _dump.push(" *xDIR-dual: ");
            _dump.push(
            std::to_string(_tcpu._ldir_dual)) ;
            _dump.push("\n");
            _dump.push(" *xOPT-dual: ");
            _dump.push(
            std::to_string(_tcpu._lopt_dual)) ;
            _dump.push("\n\n");

            _dump.push("  TOPO-FLIP: ");
            _dump.push(
            std::to_string(_tcpu._topo_flip)) ;
            _dump.push("\n");

            _dump.push("  TOPO-ZIPS: ");
            _dump.push(
            std::to_string(_tcpu._topo_zips)) ;
            _dump.push("\n");

            _dump.push("\n");
        }
        else
        {
            _dump.push("\n");
        }
    }

    } ;


    }



