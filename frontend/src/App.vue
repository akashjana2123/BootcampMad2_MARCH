<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>

    <template v-if="isAuthenticated && userRole=== 'user'">
      <router-link to="/user-dashboard">UserDashboard
      </router-link>
    </template>
    <template v-if="isAuthenticated">
      <button @click="logout">Logout</button>
    </template>
  </nav>
  <router-view/>
</template>


<script>
import axios from 'axios';

export default{
  data(){
    return{
      isAuthenticated:false,
      userRole:null
    }
  },
  created(){
    this.checkAuth();
  },
  methods:{
    checkAuth(){
      const token = localStorage.getItem('access_token')
      const user = JSON.parse(localStorage.getItem("user"))

      if (token && user){
        this.isAuthenticated = true;
        this.userRole = user.role;
      } else{
        this.isAuthenticated= false;
        this.userRole = null;
      }
    },
    logout(){
      const access_token = localStorage.removeItem('access_token');
      axios.post('/logout',null,{
        headers:{
          Authorization: `Bearer ${access_token}`
        }
      })
      .then(()=>{
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        this.isAuthenticated=false;
        this.userRole=null;
        this.$router.push('/signup')
    })
    .catch(error =>{
      console.error(error);
    })
  }
  }
}

</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
