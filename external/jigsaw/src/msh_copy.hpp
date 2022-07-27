
/*
--------------------------------------------------------
 * MSH-COPY: copy MESH data into a tria-complex.
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
 * Last updated: 18 Jul., 2022
 *
 * Copyright 2013-2022
 * Darren Engwirda
 * d.engwirda@gmail.com
 * https://github.com/dengwirda/
 *
--------------------------------------------------------
 */

#   pragma once

#   ifndef __MSH_COPY__
#   define __MSH_COPY__

#include <math.h>

template<
        typename iptr_list
>
__normal_call void_type sort_node_tree(
        mesh_data &_mesh,
        iptr_list &_perm
) {
    iptr_type static constexpr SIZE = +256;

    if (_mesh._ndim == +2 &&
        _mesh._kind ==
        jmsh_kind::euclidean_mesh) {
        /*---------------------------------- sort 2-dim. mesh */
        typedef geom_tree::aabb_item_node_k<
                real_type,
                iptr_type, 2> tree_item;

        geom_tree::aabb_tree<
                tree_item, 2> _tree;

        containers::array<tree_item> _item;
        containers::array<iptr_type> _itmp;

        iptr_type _ipos = +0;
        for (auto _iter = _mesh.
                _euclidean_rdel_2d._tria._nset.head();
             _iter != _mesh.
                     _euclidean_rdel_2d._tria._nset.tend();
             ++_iter, ++_ipos) {
            if (_iter->mark() >= +0) {
                _item.push_tail();
                _item.tail()->ipos() = _ipos;
                _item.tail()->pval(0) =
                        _iter->pval(0);
                _item.tail()->pval(1) =
                        _iter->pval(1);
            }
        }

        _tree.load(_item.head(), _item.tend(),
                   SIZE,  // pop.=#nodes per leaf
                   _tree.median_split,
                   1.0,    // set LONG=1, only div. by pop.
                   0.0);  // set VTOL=0, only div. by pop.

        _tree.dcmp(_itmp, _perm);
    } else if (_mesh._ndim == +3 &&
               _mesh._kind ==
               jmsh_kind::euclidean_mesh) {
        /*---------------------------------- sort 3-dim. mesh */
        typedef geom_tree::aabb_item_node_k<
                real_type,
                iptr_type, 3> tree_item;

        geom_tree::aabb_tree<
                tree_item, 3> _tree;

        containers::array<tree_item> _item;
        containers::array<iptr_type> _itmp;

        iptr_type _ipos = +0;
        for (auto _iter = _mesh.
                _euclidean_rdel_3d._tria._nset.head();
             _iter != _mesh.
                     _euclidean_rdel_3d._tria._nset.tend();
             ++_iter, ++_ipos) {
            if (_iter->mark() >= +0) {
                _item.push_tail();
                _item.tail()->ipos() = _ipos;
                _item.tail()->pval(0) =
                        _iter->pval(0);
                _item.tail()->pval(1) =
                        _iter->pval(1);
                _item.tail()->pval(2) =
                        _iter->pval(2);
            }
        }

        _tree.load(_item.head(), _item.tend(),
                   SIZE,  // pop.=#nodes per leaf
                   _tree.median_split,
                   1.0,    // set LONG=1, only div. by pop.
                   0.0);  // set VTOL=0, only div. by pop.

        _tree.dcmp(_itmp, _perm);
    }
}

template<
        typename iptr_list
>
__normal_call void_type sort_node(
        mesh_data &_mesh,
        iptr_list &_perm
) {

    class node_pair {
    public  :
        /*------------------------ tuple for cell re-ordering */
        iptr_type _node;
        int64_t _cost;

        __inline_call node_pair(iptr_type _n, int64_t _c)
                : _node(_n), _cost(_c) {}
    };

    class node_pred {
    public  :
        /*------------------------ less-than op. for cost-tup */
        __inline_call
        bool_type operator()(
                node_pair const &_idat,
                node_pair const &_jdat
        ) const {
            return _idat._cost < _jdat._cost;
        }
    };

    auto populate_perm = [& _perm](const auto &node) {
        _perm.push_tail(node._node);
    };

    auto max = -1.;
    auto min = -1.;

    auto scale = [& max, & min](const auto &val) {
        return static_cast<int32_t>(((val - min) / (max - min)) * std::numeric_limits<int32_t>::max() +
                                   std::numeric_limits<int32_t>::max());
    };

    if (_mesh._ndim == +2 &&
        _mesh._kind ==
        jmsh_kind::euclidean_mesh) {
        /*---------------------------------- sort 2-dim. mesh */

        iptr_type _ipos = +0;

        containers::array<node_pair> node_pairs;
        node_pairs.set_alloc(_mesh._euclidean_rdel_2d._tria._nset.count());

        // sep minmax per x,y,z

        auto minimax = [& max, & min](const auto &node) {
            const auto a = node.pval(0);
            const auto b = node.pval(1);
            const auto [n, x] = std::minmax({a, b});
            max = max > x ? max : x;
            min = min < n ? min : n;
        };

        std::for_each(_mesh._euclidean_rdel_2d._tria._nset.head(),
                      _mesh._euclidean_rdel_2d._tria._nset.tend(), minimax);

        auto morton2D = [](const auto x, const auto y) {
            int64_t answer = 0;
            unsigned int checkbits = (unsigned int) floor(sizeof(int64_t) * 4.0f);
            for (unsigned int i = 0; i < checkbits; ++i) {
                int64_t mshifted = static_cast<int64_t>(0x1) << i;
                unsigned int shift = i;
                answer |=
                        ((x & mshifted) << shift)
                        | ((y & mshifted) << (shift + 1));
            }
            return answer;
        };

        auto populate_npairs = [& max, & min, & node_pairs, & _ipos, & morton2D, & scale](const auto &node) {
            if (node.mark() >= 0) {
                node_pairs.push_tail(node_pair(_ipos, morton2D(scale(node.pval(0)), scale(node.pval(1)))));
            }
            ++_ipos;
        };

        std::for_each(_mesh._euclidean_rdel_2d._tria._nset.head(),
                      _mesh._euclidean_rdel_2d._tria._nset.tend(), populate_npairs);

        algorithms::qsort(node_pairs.head(),
                          node_pairs.tend(),
                          node_pred());

        std::for_each(node_pairs.head(), node_pairs.tend(), populate_perm);

    } else if (_mesh._ndim == +3 &&
               _mesh._kind ==
               jmsh_kind::euclidean_mesh) {
        iptr_type _ipos = +0;

        containers::array<node_pair> node_pairs;
        node_pairs.set_alloc(_mesh._euclidean_rdel_3d._tria._nset.count());

        auto minimax = [& max, & min](const auto &node) {
            const auto a = node.pval(0);
            const auto b = node.pval(1);
            const auto c = node.pval(2);
            const auto [n, x] = std::minmax({a, b, c});
            max = max > x ? max : x;
            min = min < n ? min : n;
        };

        std::for_each(_mesh._euclidean_rdel_3d._tria._nset.head(),
                      _mesh._euclidean_rdel_3d._tria._nset.tend(), minimax);

        auto morton3D = [](const auto x, const auto y, const auto z) {
            int64_t answer = 0;
            unsigned int checkbits = (sizeof(int64_t) * 8) / 3;
            for (unsigned int i = 0; i < checkbits; ++i) {
                int64_t mshifted = static_cast<int64_t>(1) << i;
                unsigned int shift = 2 * i;
                answer |= ((x & mshifted) << shift)
                          | ((y & mshifted) << (shift + 1))
                          | ((z & mshifted) << (shift + 2));
            }
            return answer;
        };

        auto populate_npairs = [& max, & min, & node_pairs, & _ipos, & morton3D, & scale](const auto &node) {
            if (node.mark() >= 0) {
                node_pairs.push_tail(
                        node_pair(_ipos, morton3D(scale(node.pval(0)), scale(node.pval(1)), scale(node.pval(2)))));
            }
            ++_ipos;
        };

        std::for_each(_mesh._euclidean_rdel_3d._tria._nset.head(),
                      _mesh._euclidean_rdel_3d._tria._nset.tend(), populate_npairs);

        algorithms::qsort(node_pairs.head(),
                          node_pairs.tend(),
                          node_pred());

        std::for_each(node_pairs.head(), node_pairs.tend(), populate_perm);


    }
}


template<
        typename cell_list,
        typename iptr_list,
        typename cell_perm
>
__normal_call void_type sort_cell(
        cell_list &_cell,
        size_t _nsiz,
        iptr_list &_nmap,
        cell_perm &_perm
) {
    class cell_cost {
    public  :
        /*------------------------ tuple for cell re-ordering */
        typename cell_list::item_type *
                _cell;
        float _cost;

        /*------------------------ construct inline from src. */
        __inline_call cell_cost(
                typename cell_list::item_type *
                _psrc,
                float const &_csrc
        ) :
                _cell(_psrc),
                _cost((float) _csrc) {}
    };

    class cell_pred {
    public  :
        /*------------------------ less-than op. for cost-tup */
        __inline_call
        bool_type operator()(
                cell_cost const &_idat,
                cell_cost const &_jdat
        ) const {
            return _idat._cost < _jdat._cost;
        }
    };

    typedef
    containers::array<cell_cost> cost_list;

    cost_list _sort;
    for (auto _iter = _cell._lptr.head();
         _iter != _cell._lptr.tend();
         ++_iter) {
        for (auto _item = *_iter;
             _item != nullptr;
             _item = _item->_next) {
            float _cost = +0.;
            for (auto
                         _inod = _nsiz; _inod-- != 0;) {
                _cost += _nmap[
                        _item->_data._node[_inod]];
            }

            _sort.push_tail(cell_cost(
                    _item, _cost / _nsiz));
        }
    }

    algorithms::qsort(_sort.head(),
                      _sort.tend(),
                      cell_pred());

    for (auto _iter = _sort.head();
         _iter != _sort.tend();
         ++_iter) {
        _perm.push_tail(_iter->_cell);
    }
}


/*
--------------------------------------------------------
 * COPY-MESH: copy rdel-complex to tria-complex.
--------------------------------------------------------
 */

template<
        typename jlog_data
>
__normal_call iptr_type copy_mesh(
        jcfg_data &_jcfg,
        jlog_data &_jlog,
        mesh_data &_mesh
) {
    iptr_type _errv = __no_error;

    __unreferenced(_jcfg);
    __unreferenced(_jlog);

    if (_mesh._ndim == +2 &&
        _mesh._kind ==
        jmsh_kind::euclidean_mesh) {
        /*---------------------------------- copy 2-dim. mesh */
        containers::array<iptr_type> _nmap, _perm;

        sort_node(_mesh, _perm);

        _nmap.set_count(_mesh.
                                _euclidean_rdel_2d._tria._nset.count(),
                        containers::loose_alloc, -1);

        _mesh._euclidean_mesh_2d._mesh.
                clear(containers::tight_alloc);

        for (auto _iter = _perm.head();
             _iter != _perm.tend();
             ++_iter) {
            auto _nptr = _mesh.
                    _euclidean_rdel_2d._tria._nset.head() + *_iter;

            typename mesh_data::
            euclidean_mesh_2d::
            mesh_type::node_type _node;
            _node.pval(0) = _nptr->pval(0);
            _node.pval(1) = _nptr->pval(1);

            _node.pval(2) = _nptr->pval(2);

            _node.hidx() = _nptr->idxh();

            _node.itag() = _nptr->part();
            _node.fdim() = _nptr->fdim();
            _node.feat() = _nptr->feat();

            _nmap[*_iter] =
                    _mesh._euclidean_mesh_2d.
                            _mesh.push_node(_node, false);
        }

        _mesh._euclidean_rdel_2d._tria.
                clear(containers::tight_alloc);

        containers::array<
                mesh_data::euclidean_rdel_2d::
                edge_list::item_type *> _eprm;

        sort_cell(_mesh.
                _euclidean_rdel_2d._eset, +2, _nmap, _eprm);

        for (auto _iter = _eprm.head();
             _iter != _eprm.tend();
             ++_iter) {
            auto _item = *_iter;

            typename mesh_data::
            euclidean_mesh_2d::
            mesh_type::edge_type _face;
            _face.node(0) =
                    _nmap[_item->_data._node[0]];
            _face.node(1) =
                    _nmap[_item->_data._node[1]];

            _face.itag() =
                    _item->_data._part;

            _mesh._euclidean_mesh_2d.
                    _mesh.push_edge(_face, false);
        }

        _mesh._euclidean_rdel_2d._eset.
                clear(containers::tight_alloc);

        containers::array<
                mesh_data::euclidean_rdel_2d::
                tria_list::item_type *> _tprm;

        sort_cell(_mesh.
                _euclidean_rdel_2d._tset, +3, _nmap, _tprm);

        for (auto _iter = _tprm.head();
             _iter != _tprm.tend();
             ++_iter) {
            auto _item = *_iter;

            typename mesh_data::
            euclidean_mesh_2d::
            mesh_type::tri3_type _face;
            _face.node(0) =
                    _nmap[_item->_data._node[0]];
            _face.node(1) =
                    _nmap[_item->_data._node[1]];
            _face.node(2) =
                    _nmap[_item->_data._node[2]];

            _face.itag() =
                    _item->_data._part;

            _mesh._euclidean_mesh_2d.
                    _mesh.push_tri3(_face, false);
        }

        _mesh._euclidean_rdel_2d._tset.
                clear(containers::tight_alloc);

        _mesh._euclidean_rdel_2d.
                clear(containers::tight_alloc);

        _mesh._euclidean_mesh_2d.
                _mesh.make_link();

    } else if (_mesh._ndim == +3 &&
               _mesh._kind ==
               jmsh_kind::euclidean_mesh) {
        /*---------------------------------- copy 3-dim. mesh */
        containers::array<iptr_type> _nmap, _perm;

        sort_node(_mesh, _perm);

        _nmap.set_count(_mesh.
                                _euclidean_rdel_3d._tria._nset.count(),
                        containers::loose_alloc, -1);

        _mesh._euclidean_mesh_3d._mesh.
                clear(containers::tight_alloc);

        for (auto _iter = _perm.head();
             _iter != _perm.tend();
             ++_iter) {
            auto _nptr = _mesh.
                    _euclidean_rdel_3d._tria._nset.head() + *_iter;

            typename mesh_data::
            euclidean_mesh_3d::
            mesh_type::node_type _node;
            _node.pval(0) = _nptr->pval(0);
            _node.pval(1) = _nptr->pval(1);
            _node.pval(2) = _nptr->pval(2);

            _node.pval(3) = _nptr->pval(3);

            _node.hidx() = _nptr->idxh();

            _node.itag() = _nptr->part();
            _node.fdim() = _nptr->fdim();
            _node.feat() = _nptr->feat();

            _nmap[*_iter] =
                    _mesh._euclidean_mesh_3d.
                            _mesh.push_node(_node, false);
        }

        _mesh._euclidean_rdel_3d._tria.
                clear(containers::tight_alloc);

        containers::array<
                mesh_data::euclidean_rdel_3d::
                edge_list::item_type *> _eprm;

        sort_cell(_mesh.
                _euclidean_rdel_3d._eset, +2, _nmap, _eprm);

        for (auto _iter = _eprm.head();
             _iter != _eprm.tend();
             ++_iter) {
            auto _item = *_iter;

            typename mesh_data::
            euclidean_mesh_3d::
            mesh_type::edge_type _face;
            _face.node(0) =
                    _nmap[_item->_data._node[0]];
            _face.node(1) =
                    _nmap[_item->_data._node[1]];

            _face.itag() =
                    _item->_data._part;

            _mesh._euclidean_mesh_3d.
                    _mesh.push_edge(_face, false);
        }

        _mesh._euclidean_rdel_3d._eset.
                clear(containers::tight_alloc);

        containers::array<
                mesh_data::euclidean_rdel_3d::
                face_list::item_type *> _fprm;

        sort_cell(_mesh.
                _euclidean_rdel_3d._fset, +3, _nmap, _fprm);

        for (auto _iter = _fprm.head();
             _iter != _fprm.tend();
             ++_iter) {
            auto _item = *_iter;

            typename mesh_data::
            euclidean_mesh_3d::
            mesh_type::tri3_type _face;
            _face.node(0) =
                    _nmap[_item->_data._node[0]];
            _face.node(1) =
                    _nmap[_item->_data._node[1]];
            _face.node(2) =
                    _nmap[_item->_data._node[2]];

            _face.itag() =
                    _item->_data._part;

            _mesh._euclidean_mesh_3d.
                    _mesh.push_tri3(_face, false);
        }

        _mesh._euclidean_rdel_3d._fset.
                clear(containers::tight_alloc);

        containers::array<
                mesh_data::euclidean_rdel_3d::
                tria_list::item_type *> _tprm;

        sort_cell(_mesh.
                _euclidean_rdel_3d._tset, +4, _nmap, _tprm);

        for (auto _iter = _tprm.head();
             _iter != _tprm.tend();
             ++_iter) {
            auto _item = *_iter;

            typename mesh_data::
            euclidean_mesh_3d::
            mesh_type::tri4_type _face;
            _face.node(0) =
                    _nmap[_item->_data._node[0]];
            _face.node(1) =
                    _nmap[_item->_data._node[1]];
            _face.node(2) =
                    _nmap[_item->_data._node[2]];
            _face.node(3) =
                    _nmap[_item->_data._node[3]];

            _face.itag() =
                    _item->_data._part;

            _mesh._euclidean_mesh_3d.
                    _mesh.push_tri4(_face, false);
        }

        _mesh._euclidean_rdel_3d._tset.
                clear(containers::tight_alloc);

        _mesh._euclidean_rdel_3d.
                clear(containers::tight_alloc);

        _mesh._euclidean_mesh_3d.
                _mesh.make_link();

    }

    return (_errv);
}


#   endif   //__MSH_COPY__



