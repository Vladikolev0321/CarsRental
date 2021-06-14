<template>
  <div class="hello">
    
  </div>
</template>

<script>
export default {
      name: "Login",
      data() {
        return {
          username: "",
          password: "",
          proccessing: false,
          message: ""
        };
      },
      methods: {
        login: function() {
          this.loading = true;
          this.axios
            .post("/api/login", {
              username: this.username,
              password: this.password
            })
            .then(response => {
              if (response.data.status == "success") {
                this.proccessing = false;
                this.$emit("authenticated", true, response.data.data);
              } else {
                this.message = "Login Faild, try again";
              }
            })
            .catch(error => {
              this.message = "Login Faild, try again";
              this.proccessing = false;
            });
        }
      }
};
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
