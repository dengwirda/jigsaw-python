
    __static_call
    __normal_call void_type part_mesh (
        mesh_type &_mesh,  // full mesh obj.
        part_sets &_part,  // partition data-structure
        iptr_type  _nprt   // number of partitions to make
        )
    {

    if (_nprt > 1) {// define type of item to store in the tree
        typedef geom_tree::aabb_item_node_k<
                real_type,
                iptr_type,
                pred_type::geom_dims> tree_item;

        // define type of tree, using tree item def
        geom_tree::aabb_tree<
                tree_item,
                pred_type::geom_dims> _tree;

        // an array of items to load into the tree
        containers::array<tree_item> _item;

        auto _nblk =  // no. nodes per part for nprt
                (8 * _mesh.node().count()) / _nprt / 3;

        // populate item array to load:
        // cartesian position of mesh node +
        // index position into mesh node array
        iptr_type _ipos = +0;
        for (auto _iter = _mesh.node().head();
             _iter != _mesh.node().tend();
             ++_iter, ++_ipos) {
            if (_iter->mark() >= 0 && _iter->ndeg(TRIA3_tag) > 0) {
                _item.push_tail();
                _item.tail()->ipos() = _ipos;

                for (auto _idim = geom_dims;
                     _idim-- != 0;)
                    _item.tail()->pval(_idim) =
                            _iter->pval(_idim);
            }
        }

        // load items into tree and bisect
        // split until leaves contain approx nblk items
        _tree.load(_item.head(), _item.tend(), _nblk,
                   _tree.median_split,
                   1.0,    // set LONG=1, only div. by pop.
                   0.0);  // set VTOL=0, only div. by pop.

        // pull item indexing out of tree and make mesh
        // partition

        // LPTR and LIST define a set of "sparse" lists
        // LIST[LPTR[K]:LPTR[K+1]-1] contains the nodes
        // in the K-th partition
        _part._lptr.clear();
        _part._list.clear();
        _part._part.clear();
        _part._itfc.clear();
        _part._ifls.clear();
        _part._trls.clear();
        _part._seqs.clear();

        _tree.dcmp(_part._lptr, _part._list);

        std::cout << "number of parts: "
                  << _part._lptr.count() - 1 << std::endl;

        // also build indexing the other way around:
        // PART[J] = K is partition for J-th mesh node
        _part._part.set_count(_mesh.node().count(),
                              containers::tight_alloc, (iptr_type) -1);
        _part._trls.set_count(_mesh.tri3().count(),
                              containers::tight_alloc,
                              std::numeric_limits<iptr_type>::min());
        _part._seqs.set_count(_nprt, containers::tight_alloc, 0);

        for (auto _list = (size_t) 0;
             _list < _part._lptr.count() - 1; ++_list) {
            std::cout << "size of part: " <<
                      _part._lptr[_list + 1] - _part._lptr[_list + 0] << std::endl;

            for (auto _iptr = _part._lptr[_list + 0];
                 _iptr < _part._lptr[_list + 1];
                 ++_iptr)
                _part._part[_part._list[_iptr]] = _list;
        }
        _part._itfc.set_count(_mesh.node().count(), containers::tight_alloc, (bool_type) 0);
        // 3D Case


        // Interface Set ..?
        // --
        for (auto _iter = _mesh.tri3().head(); _iter != _mesh.tri3().tend(); ++_iter) {
            if (_iter->mark() >= 0) {
                auto i = _iter->node(0);
                auto j = _iter->node(1);
                auto k = _iter->node(2);
                auto l = _part._part[i];
                auto m = _part._part[j];
                auto n = _part._part[k];
                auto o = m == l && l == n;
                if (o)
                    _part._trls[_iter - _mesh.tri3().head()] = l;
                else {
                    _part._itfc[i] = 1;
                    _part._itfc[j] = 1;
                    _part._itfc[k] = 1;
                    if (m != l && l != n)
                        _part._trls[_iter - _mesh.tri3().head()] = std::numeric_limits<iptr_type>::min() + 1;
                    else {
                        auto p = std::min({l, m, n});
                        _part._seqs[p] = 1;
                        _part._trls[_iter - _mesh.tri3().head()] = -1 - p;
                    }

                }
            }
        }

        for (auto _iter = _part._itfc.head(); _iter != _part._itfc.tend(); ++_iter)
            if (*_iter == 1)
                _part._ifls.push_tail(_iter - _part._itfc.head());
    } else {
        _part._lptr.clear();
        _part._list.clear();
        _part._part.clear();
        _part._itfc.clear();
        _part._ifls.clear();
        _part._trls.clear();
        _part._seqs.clear();
        _part._part.set_count(_mesh.node().count(),
                              containers::tight_alloc, (iptr_type) 0);
        _part._trls.set_count(_mesh.tri3().count(),
                              containers::tight_alloc,
                              0);
        _part._seqs.set_count(_nprt, containers::tight_alloc, 0);
        _part._lptr.push_tail(0);
        _part._lptr.push_tail(_mesh.node().count());
    }

    // just for temp. debug checks:
    // write partition index to ID space in mesh node
    // struct., will be written to output file for 
    // external checking 

	auto _ipos = +0;
        for (auto _iter  = _mesh.node().head();
                  _iter != _mesh.node().tend();
                ++_iter, ++_ipos)
        {
            if (_iter->mark() >= 0)
            {
                _iter->itag() = _part._part[_ipos];
            }
        }

    }

    __static_call
    __normal_call void_type part_mesh (
            mesh_type &_mesh,  // full mesh obj.
            part_sets &_part,  // partition data-structure
            iptr_type  _nprt,   // number of partitions to make
            iptr_list  _aset
    )
    {

        if (_nprt > 1) {// define type of item to store in the tree
            typedef geom_tree::aabb_item_node_k<
            real_type,
            iptr_type,
            pred_type::geom_dims> tree_item;

            // define type of tree, using tree item def
            geom_tree::aabb_tree<
            tree_item,
            pred_type::geom_dims> _tree;

            // an array of items to load into the tree
            containers::array<tree_item> _item;

            auto _nblk =  // no. nodes per part for nprt
                    (8 * _aset.count()) / _nprt / 3;

            // populate item array to load:
            // cartesian position of mesh node +
            // index position into mesh node array
            iptr_type _ipos = +0;
            for (auto _ape = _aset.head();
                 _ape != _aset.tend();
                 ++_ape, ++_ipos) {

                auto _iter = _mesh.node().head() + * _ape;

                if (_iter->mark() >= 0 && _iter->ndeg(TRIA3_tag) > 0) {
                    _item.push_tail();
                    _item.tail()->ipos() = * _ape;

                    for (auto _idim = geom_dims;
                         _idim-- != 0;)
                        _item.tail()->pval(_idim) =
                                _iter->pval(_idim);
                }
            }

            // load items into tree and bisect
            // split until leaves contain approx nblk items
            _tree.load(_item.head(), _item.tend(), _nblk,
                       _tree.median_split,
                       1.0,    // set LONG=1, only div. by pop.
                       0.0);  // set VTOL=0, only div. by pop.

            // pull item indexing out of tree and make mesh
            // partition

            // LPTR and LIST define a set of "sparse" lists
            // LIST[LPTR[K]:LPTR[K+1]-1] contains the nodes
            // in the K-th partition
            _part._lptr.clear();
            _part._list.clear();
            _part._part.clear();
            _part._itfc.clear();
            _part._ifls.clear();
            _part._trls.clear();
            _part._seqs.clear();

            _tree.dcmp(_part._lptr, _part._list);

            std::cout << "number of parts: "
                      << _part._lptr.count() - 1 << std::endl;

            // also build indexing the other way around:
            // PART[J] = K is partition for J-th mesh node
            _part._part.set_count(_mesh.node().count(),
                                  containers::tight_alloc, (iptr_type) -1);
            _part._trls.set_count(_mesh.tri3().count(),
                                  containers::tight_alloc,
                                  std::numeric_limits<iptr_type>::min());
            _part._seqs.set_count(_nprt, containers::tight_alloc, 0);

            for (auto _list = (size_t) 0;
                 _list < _part._lptr.count() - 1; ++_list) {
                std::cout << "size of part: " <<
                          _part._lptr[_list + 1] - _part._lptr[_list + 0] << std::endl;

                for (auto _iptr = _part._lptr[_list + 0];
                     _iptr < _part._lptr[_list + 1];
                     ++_iptr)
                    _part._part[_part._list[_iptr]] = _list;
            }
            _part._itfc.set_count(_mesh.node().count(), containers::tight_alloc, (bool_type) 0);
            // 3D Case
            // Interface Set ..?
            // --
            for (auto _iter = _mesh.tri3().head(); _iter != _mesh.tri3().tend(); ++_iter) {
                if (_iter->mark() >= 0) {
                    auto i = _iter->node(0);
                    auto j = _iter->node(1);
                    auto k = _iter->node(2);
                    auto l = _part._part[i];
                    auto m = _part._part[j];
                    auto n = _part._part[k];
                    auto o = m == l && l == n;
                    if (o)
                        _part._trls[_iter - _mesh.tri3().head()] = l;
                    else {
                        _part._itfc[i] = 1;
                        _part._itfc[j] = 1;
                        _part._itfc[k] = 1;
                        auto p = -1;

                        // Sorry for this code. Yikes, it's bad!
                        if (l == -1 && m == -1 && n == -1)
                            _part._trls[_iter - _mesh.tri3().head()] = std::numeric_limits<iptr_type>::min();
                        else if (l == -1 || m == -1 || n == -1) {
                            if (l * m * n < 0) { // True if only 1 negative
                                p = m >= 0 ? m : l; // chooses the positive
                                _part._trls[_iter - _mesh.tri3().head()] = p;
                            } else { // Only if 2 negatives
                                p = std::max({l, m, n});
                                _part._seqs[p] = 1;
                                _part._trls[_iter - _mesh.tri3().head()] = -1 - p;
                            }
                        } else if (m != l && l != n) // No negatives, strictly sequential portion
                            _part._trls[_iter - _mesh.tri3().head()] = std::numeric_limits<iptr_type>::min() + 1;
                        else { // No negatives, parallel interface portion
                            p = std::min({l, m, n});
                            _part._seqs[p] = 1;
                            _part._trls[_iter - _mesh.tri3().head()] = -1 - p;
                        }
                    }
                }
            }

            for (auto _iter = _part._itfc.head(); _iter != _part._itfc.tend(); ++_iter)
                if (*_iter == 1)
                    _part._ifls.push_tail(_iter - _part._itfc.head());
        } else {
            _part._lptr.clear();
            _part._list.clear();
            _part._part.clear();
            _part._itfc.clear();
            _part._ifls.clear();
            _part._trls.clear();
            _part._seqs.clear();
            _part._part.set_count(_mesh.node().count(),
                                  containers::tight_alloc, (iptr_type) 0);
            _part._trls.set_count(_mesh.tri3().count(),
                                  containers::tight_alloc,
                                  0);
            _part._seqs.set_count(_nprt, containers::tight_alloc, 0);
            _part._lptr.push_tail(0);
            _part._lptr.push_tail(_mesh.node().count());
        }

        // just for temp. debug checks:
        // write partition index to ID space in mesh node
        // struct., will be written to output file for
        // external checking

	auto _ipos = +0;
        for (auto _iter  = _mesh.node().head();
                  _iter != _mesh.node().tend();
                ++_iter, ++_ipos)
        {
            if (_iter->mark() >= 0)
            {
                _iter->itag() = _part._part[_ipos];
            }
        }

    }

    __static_call
    __normal_call void_type part_mesh (
            mesh_type &_mesh,  // full mesh obj.
            part_sets &_pone,  // partition data-structure
            part_sets &_ptwo,
            bool_list scratch,
            iptr_type  _nprt // number of partitions to make

    )
    {
            part_mesh(_mesh, _pone, _nprt);

            for (auto it = _mesh.tri3().head(); it != _mesh.tri3().tend(); ++ it) {
                auto i = it->node(0);
                auto j = it->node(1);
                auto k = it->node(2);
                if (it->mark() >= 0 && (_pone._itfc[i] == 1 || _pone._itfc[j] == 1 || _pone._itfc[k] == 1)) {
                    _pone._trls[it - _mesh.tri3().head()] = std::numeric_limits<iptr_type>::min() + 1;
                    scratch[i] = 1;
                    scratch[j] = 1;
                    scratch[k] = 1;
                }
            }

            typedef geom_tree::aabb_item_node_k<
                    real_type,
                    iptr_type,
                    pred_type::geom_dims> tree_item;

            // define type of tree, using tree item def
            geom_tree::aabb_tree<
                    tree_item,
                    pred_type::geom_dims> _tree;

            // an array of items to load into the tree
            containers::array<tree_item> _item;

            auto _nblk =  // no. nodes per part for nprt
                    (8 * std::accumulate(scratch.head(), scratch.tend(), 0)) / _nprt / 3;

            // populate item array to load:
            // cartesian position of mesh node +
            // index position into mesh node array
            iptr_type _ipos = +0;
            for (auto _iter = _mesh.node().head();
                 _iter != _mesh.node().tend();
                 ++_iter, ++_ipos) {
                if (_iter->mark() >= 0 && _iter->ndeg(TRIA3_tag) > 0 && scratch[_ipos] == 1) {
                    _item.push_tail();
                    _item.tail()->ipos() = _ipos;

                    for (auto _idim = geom_dims;
                         _idim-- != 0;)
                        _item.tail()->pval(_idim) =
                                _iter->pval(_idim);
                }
            }

            // load items into tree and bisect
            // split until leaves contain approx nblk items
            _tree.load(_item.head(), _item.tend(), _nblk,
                       _tree.median_split,
                       1.0,    // set LONG=1, only div. by pop.
                       0.0);  // set VTOL=0, only div. by pop.

            // pull item indexing out of tree and make mesh
            // partition

            // LPTR and LIST define a set of "sparse" lists
            // LIST[LPTR[K]:LPTR[K+1]-1] contains the nodes
            // in the K-th partition
            _ptwo._lptr.clear();
            _ptwo._list.clear();
            _ptwo._part.clear();
            _ptwo._itfc.clear();
            _ptwo._ifls.clear();
            _ptwo._trls.clear();
            _ptwo._seqs.clear();

            _tree.dcmp(_ptwo._lptr, _ptwo._list);

            std::cout << "number of parts: "
                      << _ptwo._lptr.count() - 1 << std::endl;

            // also build indexing the other way around:
            // PART[J] = K is partition for J-th mesh node
            _ptwo._part.set_count(_mesh.node().count(),
                                  containers::tight_alloc, (iptr_type) -1);
            _ptwo._trls.set_count(_mesh.tri3().count(),
                                  containers::tight_alloc,
                                  std::numeric_limits<iptr_type>::min());
            _ptwo._seqs.set_count(_nprt, containers::tight_alloc, 0);

            for (auto _list = (size_t) 0;
                 _list < _ptwo._lptr.count() - 1; ++_list) {
                std::cout << "size of part: " <<
                          _ptwo._lptr[_list + 1] - _ptwo._lptr[_list + 0] << std::endl;

                for (auto _iptr = _ptwo._lptr[_list + 0];
                     _iptr < _ptwo._lptr[_list + 1];
                     ++_iptr)
                    _ptwo._part[_ptwo._list[_iptr]] = _list;
            }
            _ptwo._itfc.set_count(_mesh.node().count(), containers::tight_alloc, (bool_type) 0);
            bool_list node_scratch;
            node_scratch.set_count(_mesh.node().count(), containers::tight_alloc, 0);
            // 3D Case
            // Interface Set ..?
            for (auto _iter = _mesh.tri3().head(); _iter != _mesh.tri3().tend(); ++_iter) {
                if (_iter->mark() >= 0 && _pone._trls[_iter - _mesh.tri3().head()] == std::numeric_limits<iptr_type>::min() + 1) {
                    auto i = _iter->node(0);
                    auto j = _iter->node(1);
                    auto k = _iter->node(2);
                    auto l = _ptwo._part[i];
                    auto m = _ptwo._part[j];
                    auto n = _ptwo._part[k];
                    auto o = m == l && l == n;
                    if (o)
                        _ptwo._trls[_iter - _mesh.tri3().head()] = l;
                    else {
                        _ptwo._itfc[i] = 1;
                        _ptwo._itfc[j] = 1;
                        _ptwo._itfc[k] = 1;
                        if (m != l && l != n) {
                            _ptwo._trls[_iter - _mesh.tri3().head()] = std::numeric_limits<iptr_type>::min() + 1;
                            node_scratch[i] = 1;
                            node_scratch[j] = 1;
                            node_scratch[k] = 1;
                        }
                        else {
                            auto p = std::min({l, m, n});
                            _ptwo._seqs[p] = 1;
                            _ptwo._trls[_iter - _mesh.tri3().head()] = -1 - p;
                        }
                    }
                }
            }

        for (auto it = _mesh.tri3().head(); it != _mesh.tri3().tend(); ++ it) {
            auto i = it->node(0);
            auto j = it->node(1);
            auto k = it->node(2);
            if (it->mark() >= 0 && (node_scratch[i] == 1 || node_scratch[j] == 1 || node_scratch[k] == 1))
                _ptwo._trls[it - _mesh.tri3().head()] = std::numeric_limits<iptr_type>::min() + 1;
        }

            for (auto _iter = _ptwo._itfc.head(); _iter != _ptwo._itfc.tend(); ++_iter)
                if (*_iter == 1)
                    _ptwo._ifls.push_tail(_iter - _ptwo._itfc.head());

            for (size_t i = 0; i < _pone._itfc.count(); ++ i)
                _pone._itfc[i] = scratch[i];

//        auto _ipos = +0;
//        for (auto _iter  = _mesh.node().head();
//             _iter != _mesh.node().tend();
//             ++_iter, ++_ipos)
//        {
//            if (_iter->mark() >= 0)
//            {
//                _iter->itag() = _ptwo._part[_ipos];
//            }
//        }
    }
    
