import { createStore } from 'vuex';
import api from '@/utils/axios';
import { encrypt, decrypt, encryptToken, decryptToken } from '@/utils/crypto';

function getDecryptedToken() {
  try {
    const encryptedToken = localStorage.getItem('access_token');
    return encryptedToken ? decryptToken(encryptedToken) : '';
  } catch {
    return '';
  }
}

function getDecryptedUser() {
  try {
    const rawUser = localStorage.getItem('user');
    return rawUser ? decrypt(rawUser) : {};
  } catch {
    return {};
  }
}

export default createStore({
  state: {
    token: getDecryptedToken(),
    user: getDecryptedUser(),
    authChecked: false,
  },
  mutations: {
    clearToken(state) {
      state.token = '';
      localStorage.removeItem('access_token');
    },
    setToken(state, token) {
      state.token = token;
      try {
        const encrypted = encryptToken(token);
        localStorage.setItem('access_token', encrypted);
      } catch (e) {
        console.warn('Ошибка при шифровании токена:', e);
      }
    },
    setUser(state, user) {
      state.user = user;
      try {
        const encryptedUser = encrypt(user);
        localStorage.setItem('user', encryptedUser);
      } catch (e) {
        console.warn('Ошибка при шифровании user:', e);
      }
    },
    logout(state) {
      state.token = '';
      state.user = {};
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    },
    setAuthChecked(state, value) {
      state.authChecked = value;
    },
  },
  actions: {
    login({ commit }, { token, user }) {
      commit('setToken', token);
      commit('setUser', user);
      commit('setAuthChecked', true);
    },
    logout({ commit }) {
      commit('logout');
      commit('setAuthChecked', true);
    },
    async checkToken({ commit }) {
      const token = getDecryptedToken();

      if (!token) {
        commit('logout');
        commit('setAuthChecked', true);
        return;
      }

      try {
        const response = await api.get('/validate_token');

        if (response.data.valid) {
          const user = getDecryptedUser();
          commit('setUser', user);
          commit('setToken', token);
        } else {
          commit('logout');
        }
      } catch (e) {
        console.warn('Ошибка при проверке токена:', e);
        commit('logout');
      } finally {
        commit('setAuthChecked', true);
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
    },
    isAuthChecked(state) {
      return state.authChecked;
    }
  }
});
