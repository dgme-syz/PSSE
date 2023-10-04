import { createStore } from 'vuex'

const store = createStore({
  state: {
    loggedIn: true,// 注意初始化默认值
    EmptyCarPostion:0,
    BeforeOneHourIncome:0,
    BeforeOneDayIncome:0,
    BeforeOneMonthIncome:0,
  },
  getters: {
    getVariable(state) {
      return state.loggedIn;
    },
    getIncomeInfo(state) {
      var formData = {
        ECP : state.EmptyCarPostion,
        BOHI : state.BeforeOneHourIncome,
        BODI : state.BeforeOneDayIncome,
        BOMI : state.BeforeOneMonthIncome,  
      };
      return formData;
    }
  },
  mutations: {
    setloggedIn(state, new_state) {
      console.log('ok');
      state.loggedIn = new_state;
    },
    setIncomInfo(state, form) {
      console.log('update income');
      state.EmptyCarPostion = form.ECP;
      state.BeforeOneDayIncome = form.BODI;
      state.BeforeOneHourIncome = form.BOHI;
      state.BeforeOneMonthIncome = form.BOMI;
    },
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