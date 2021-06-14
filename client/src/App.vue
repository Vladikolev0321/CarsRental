<template>
  <div id="app">
  </div>
</template>

<script>

import MessageInput from "./components/MessageInput.vue";
import Messages from "./components/Messages.vue";
import NavBar from "./components/NavBar.vue";
import Login from "./components/Login.vue";
import Users from "./components/Users.vue";
import Pusher from "pusher-js";

let pusher;

export default {
  name: "app",
  components: {
    MessageInput,
    NavBar,
    Messages,
    Users,
    Login
  },
  data: function() {
    return {
      authenticated: false,
      messages: {},
      users: [],
      active_chat_id: null,
      active_chat_index: null,
      logged_user_id: null,
      logged_user_username: null,
      current_chat_channel: null
    };
  },
  methods: {
        async setAuthenticated(login_status, user_data) {
          
          // Update the states
          this.logged_user_id = user_data.id;
          this.logged_user_username = user_data.username;
          this.authenticated = login_status;
          this.token = user_data.token;
          
          // Initialize Pusher JavaScript library
          pusher = new Pusher(process.env.VUE_APP_PUSHER_KEY, {
              cluster: process.env.VUE_APP_PUSHER_CLUSTER,
              authEndpoint: "/api/pusher/auth",
              auth: {
                headers: {
                  Authorization: "Bearer " + this.token
                }
              }
          });
          
          // Get all the users from the server
          const users = await this.axios.get("/api/users", {
            headers: { Authorization: "Bearer " + this.token }
          });
          
          // Get all users excluding the current logged user
          this.users = users.data.filter(
            user => user.userName != user_data.username
          );
    
        },
      },
};

</script>
<Users :users="users" v-on:chat="chat" />
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
