import { createStore } from 'vuex';
import api from '@/utils/axios';
import { encrypt, decrypt, encryptToken, decryptToken } from '@/utils/crypto';

function getDecryptedToken() {
  try {
    const encryptedToken = localStorage.getItem('auth_token');
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
      localStorage.removeItem('auth_token');
    },
    setToken(state, token) {
      state.token = token;
      try {
        const encrypted = encryptToken(token);
        localStorage.setItem('auth_token', encrypted);
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
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      delete api.defaults.headers.common['Authorization'];
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
      const response = await api.get('/validate_token', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.data.valid) {
        const user = getDecryptedUser();
        commit('setToken', token);
        commit('setUser', user);

        // Устанавливаем заголовок по умолчанию
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        // Можно не добавлять интерцептор здесь, если он уже добавлен в axios.js
      } else {
        commit('logout');
        // И не забудь очистить заголовок по умолчанию
        delete api.defaults.headers.common['Authorization'];
      }
    } catch (e) {
      console.warn('Ошибка при проверке токена:', e);
      commit('logout');
      delete api.defaults.headers.common['Authorization'];
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
    },
    hasRole: (state) => (role) => {
      return state.user.user_type === role;
    },
    hasWorkshop: (state) => (workshops) => {
      if (!state.user?.workshops) return false;

      if (!Array.isArray(workshops)) return false;  // <-- добавил проверку

      return workshops.some(name =>
        state.user.workshops.some(w => w.name === name)
      );
    }
  }
});
