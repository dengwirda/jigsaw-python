
    __static_call
    __normal_call void_type part_mesh (
        mesh_type &_mesh,  // full mesh obj.
        part_sets &_part,  // partition data-structure
        iptr_type  _nprt   // number of partitions to make
        )
    {

    // define type of item to store in the tree
        typedef geom_tree::aabb_item_node_k <
            real_type, 
            iptr_type, 
            pred_type::geom_dims>   tree_item ;

    // define type of tree, using tree item def
        geom_tree::aabb_tree<
            tree_item, 
            pred_type::geom_dims>  _tree;

    // an array of items to load into the tree
        containers::array<tree_item> _item;

        auto _nblk =  // no. nodes per part for nprt
        (8 * _mesh.node().count()) / _nprt / 3;

    // populate item array to load:
    // cartesian position of mesh node + 
    // index position into mesh node array
        iptr_type _ipos  = +0 ;
        for (auto _iter  = _mesh.node().head();
                  _iter != _mesh.node().tend();
                ++_iter, ++_ipos)
        {
            if (_iter->mark() >= 0)
            {
                _item.push_tail();
                _item.tail()->ipos() = _ipos;

                for (auto _idim = geom_dims; 
                          _idim-- != 0 ; )
                    _item.tail()->pval(_idim) = 
                        _iter->pval(_idim) ;
            }
        }

    // load items into tree and bisect
    // split until leaves contain approx nblk items
        _tree.load(_item.head(), _item.tend(), _nblk, 
            1.0,    // set LONG=1, only div. by pop. 
            0.0) ;  // set VTOL=0, only div. by pop.

    // pull item indexing out of tree and make mesh
    // partition

    // LPTR and LIST define a set of "sparse" lists
    // LIST[LPTR[K]:LPTR[K+1]-1] contains the nodes
    // in the K-th partition
        _part._lptr.clear();
        _part._list.clear();
        _part._part.clear();

        _tree.dcmp(_part._lptr , _part._list) ;

        std::cout << "number of parts: " 
            << _part._lptr.count() - 1 << std::endl ;

    // also build indexing the other way around:
    // PART[J] = K is partition for J-th mesh node 
        _part._part.set_count(_mesh.node().count(), 
            containers::tight_alloc, (iptr_type) -1 ) ;

        for (auto _list = (size_t)0; 
            _list < _part._lptr.count() - 1; ++_list)
        {
            std::cout << "size of part: " << 
                _part._lptr[_list+1] - _part._lptr[_list+0] << std::endl;

            for (auto _iptr = _part._lptr[_list+0];
                      _iptr < _part._lptr[_list+1];
                    ++_iptr )
            _part._part[_part._list[_iptr]] = _list ;
        }



    // just for temp. debug checks:
    // write partition index to ID space in mesh node
    // struct., will be written to output file for 
    // external checking 
        _ipos = +0;
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


