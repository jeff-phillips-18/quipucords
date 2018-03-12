import _ from 'lodash';
import {
  viewTypes,
  viewPaginationTypes,
  viewToolbarTypes,
  credentialsTypes,
  scansTypes,
  sourcesTypes
} from '../constants';

let initialState = {};

const INITAL_VIEW_STATE = {
  currentPage: 1,
  pageSize: 15,
  totalCount: 0,
  totalPages: 0,
  filterType: null,
  filterValue: '',
  activeFilters: [],
  sortType: null,
  sortField: 'name',
  sortAscending: true,
  selectedItems: [],
  expandedItems: []
};

initialState[viewTypes.SOURCES_VIEW] = Object.assign(INITAL_VIEW_STATE);
initialState[viewTypes.SCANS_VIEW] = Object.assign(INITAL_VIEW_STATE);
initialState[viewTypes.CREDENTIALS_VIEW] = Object.assign(INITAL_VIEW_STATE);

export default function viewOptionsReducer(state = initialState, action) {
  let updateState = {};

  let updatePageCounts = (viewType, itemsCount) => {
    let totalCount = itemsCount;

    // TODO: Remove this when we get decent data back in development mode
    if (process.env.NODE_ENV === 'development') {
      totalCount = Math.abs(itemsCount) % 1000;
    }

    let totalPages = Math.ceil(totalCount / state[viewType].pageSize);

    updateState[viewType] = Object.assign({}, state[viewType], {
      totalCount: totalCount,
      totalPages: totalPages,
      currentPage: Math.min(state[viewType].currentPage, totalPages || 1)
    });
  };

  const selectedIndex = function(state, item) {
    return _.findIndex(state.selectedItems, nextSelected => {
      return nextSelected.id === _.get(item, 'id');
    });
  };

  const expandedIndex = function(state, item) {
    return _.findIndex(state.expandedItems, nextExpanded => {
      return nextExpanded.id === _.get(item, 'id');
    });
  };

  switch (action.type) {
    case viewToolbarTypes.SET_FILTER_TYPE:
      if (state[action.viewType].filterType === action.filterType) {
        return state;
      }

      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        filterType: action.filterType,
        filterValue: ''
      });
      return Object.assign({}, state, updateState);

    case viewToolbarTypes.SET_FILTER_VALUE:
      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        filterValue: action.filterValue
      });
      return Object.assign({}, state, updateState);

    case viewToolbarTypes.ADD_FILTER:
      // Don't rea-add the same filter
      let filterExists = state[action.viewType].activeFilters.find(filter => {
        return action.filter.field === filter.field && action.filter.value === filter.value;
      });
      if (filterExists) {
        return state;
      }

      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        activeFilters: [...state[action.viewType].activeFilters, action.filter],
        currentPage: 1
      });
      return Object.assign({}, state, updateState);

    case viewToolbarTypes.REMOVE_FILTER:
      let index = state[action.viewType].activeFilters.indexOf(action.filter);
      if (index >= 0) {
        updateState[action.viewType] = Object.assign({}, state[action.viewType], {
          activeFilters: [
            ...state[action.viewType].activeFilters.slice(0, index),
            ...state[action.viewType].activeFilters.slice(index + 1)
          ],
          currentPage: 1
        });
        return Object.assign({}, state, updateState);
      } else {
        return state;
      }

    case viewToolbarTypes.CLEAR_FILTERS:
      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        activeFilters: [],
        currentPage: 1
      });
      return Object.assign({}, state, updateState);

    case viewToolbarTypes.SET_SORT_TYPE:
      if (state[action.viewType].sortType === action.sortType) {
        return state;
      }

      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        sortType: action.sortType,
        sortField: action.sortType.id,
        sortAscending: true,
        currentPage: 1
      });
      return Object.assign({}, state, updateState);

    case viewToolbarTypes.TOGGLE_SORT_ASCENDING:
      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        sortAscending: !state[action.viewType].sortAscending,
        currentPage: 1
      });
      return Object.assign({}, state, updateState);

    case viewPaginationTypes.VIEW_FIRST_PAGE:
      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        currentPage: 1
      });
      return Object.assign({}, state, updateState);

    case viewPaginationTypes.VIEW_LAST_PAGE:
      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        currentPage: state[action.viewType].totalPages
      });
      return Object.assign({}, state, updateState);

    case viewPaginationTypes.VIEW_PREVIOUS_PAGE:
      if (state[action.viewType].currentPage < 2) {
        return state;
      }

      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        currentPage: state[action.viewType].currentPage - 1
      });
      return Object.assign({}, state, updateState);

    case viewPaginationTypes.VIEW_NEXT_PAGE:
      if (state[action.viewType].currentPage >= state[action.viewType].totalPages) {
        return state;
      }
      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        currentPage: state[action.viewType].currentPage + 1
      });
      return Object.assign({}, state, updateState);

    case viewPaginationTypes.VIEW_PAGE_NUMBER:
      if (
        !Number.isInteger(action.pageNumber) ||
        action.pageNumber < 1 ||
        action.pageNumber > state[action.viewType].totalPages
      ) {
        return state;
      }

      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        currentPage: action.pageNumber
      });
      return Object.assign({}, state, updateState);

    case viewPaginationTypes.SET_PER_PAGE:
      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        pageSize: action.pageSize
      });
      return Object.assign({}, state, updateState);

    case credentialsTypes.GET_CREDENTIAL_FULFILLED:
    case credentialsTypes.GET_CREDENTIALS_FULFILLED:
      updatePageCounts(viewTypes.CREDENTIALS_VIEW, action.payload.data.count);
      return Object.assign({}, state, updateState);

    case sourcesTypes.GET_SOURCE_FULFILLED:
    case sourcesTypes.GET_SOURCES_FULFILLED:
      updatePageCounts(viewTypes.SOURCES_VIEW, action.payload.data.count);
      return Object.assign({}, state, updateState);

    case scansTypes.GET_SCAN_FULFILLED:
    case scansTypes.GET_SCANS_FULFILLED:
      updatePageCounts(viewTypes.SCANS_VIEW, action.payload.data.count);
      return Object.assign({}, state, updateState);

    case viewTypes.SELECT_ITEM:
      // Do nothing if it is already selected
      if (selectedIndex(state[action.viewType], action.item) !== -1) {
        return state;
      }

      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        selectedItems: [...state[action.viewType].selectedItems, action.item]
      });
      return Object.assign({}, state, updateState);

    case viewTypes.DESELECT_ITEM:
      const foundIndex = selectedIndex(state[action.viewType], action.item);

      // Do nothing if it is not already selected
      if (foundIndex === -1) {
        return state;
      }

      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        selectedItems: [
          ...state[action.viewType].selectedItems.slice(0, foundIndex),
          ...state[action.viewType].selectedItems.slice(foundIndex + 1)
        ]
      });
      return Object.assign({}, state, updateState);

    case viewTypes.EXPAND_ITEM:
      const expandIndex = expandedIndex(state[action.viewType], action.item);
      let newExpansions;

      if (expandIndex === -1) {
        newExpansions = [...state[action.viewType].expandedItems];
      } else {
        newExpansions = [
          ...state[action.viewType].expandedItems.slice(0, expandIndex),
          ...state[action.viewType].expandedItems.slice(expandIndex + 1)
        ];
      }

      if (action.expandType) {
        newExpansions.push({
          id: action.item.id,
          expandType: action.expandType
        });
      }

      updateState[action.viewType] = Object.assign({}, state[action.viewType], {
        expandedItems: newExpansions
      });
      return Object.assign({}, state, updateState);

    default:
      return state;
  }
}
