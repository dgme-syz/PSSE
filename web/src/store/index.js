import { createStore } from 'vuex'

const store = createStore({
  state: {
    loggedIn: false,
  },
  getters: {
    getVariable(state) {
      return state.loggedIn;
    }
  },
  mutations: {
    setloggedIn(state, new_state) {
      console.log('ok');
      state.loggedIn = new_state;
    }
  },
  actions: {
    updateLoggedIn({ commit }, loggedIn) {
      commit('setLoggedIn', loggedIn);
    },
  },
  modules: {
  }
})

export default store