import { createStore } from 'vuex';
import axios from 'axios';

let user = {};
try {
  const rawUser = localStorage.getItem('user');
  if (rawUser && rawUser !== 'undefined') {
    user = JSON.parse(rawUser);
  }
} catch (e) {
  console.warn('Ошибка при разборе user из localStorage:', e);
}

export default createStore({
  state: {
    token: localStorage.getItem('access_token') || '',
    user: user
  },
  mutations: {
    clearToken(state) {
      state.token = null;  // Удаляем токен
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('access_token', token);
    },
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    },
    logout(state) {
      state.token = '';
      state.user = {};
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
  },
  actions: {
    login({ commit }, { token, user }) {
      commit('setToken', token);
      commit('setUser', user);
    },
    logout({ commit }) {
      commit('logout');
    },
    // Проверка токена при запуске приложения
    checkToken({ commit }) {
      const token = localStorage.getItem('access_token');
      if (token) {
        axios
          .get('/validate_token', { headers: { Authorization: `Bearer ${token}` } })
          .then((response) => {
            if (response.data.valid) {
              // Токен валиден, можно загрузить данные пользователя
              const user = JSON.parse(localStorage.getItem('user'));
              commit('setUser', user);
            } else {
              commit('logout'); // Если токен невалиден, выходим
            }
          })
          .catch(() => {
            commit('logout'); // Ошибка на сервере или при проверке токена
          });
      } else {
        commit('logout'); // Нет токена - выходим
      }
    }
  },
  getters: {
    getToken(state) {
      return state.token;
    },
    getUser(state) {
      return state.user;
    },
    isAuthenticated(state) {
      return !!state.token;
    }
  }
});
