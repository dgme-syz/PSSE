import { createStore } from 'vuex'

const store = createStore({
  state: {
    loggedIn: false,// 注意初始化默认值
    EmptyCarPostion:10,
    BeforeOneHourIncome:10,
    BeforeOneDayIncome:10,
    BeforeOneMonthIncome:10,
    csrfToken:'',
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
    setCsrf(state, val) {
      console.log('Get csrf');
      state.csrfToken = val;
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