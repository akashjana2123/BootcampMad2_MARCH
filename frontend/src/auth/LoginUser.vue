<template>
    <div>
        <h2>
            Login
        </h2>
        <form @submit.prevent="loginUser">
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <div v-if="errorMessage">{{ errorMessage }}</div>
    </div>
</template>


<script>
import axios from 'axios';

export default{
    data(){
        return{
            username:'',
            password:'',
            errorMessage:''
        }
    },
    methods:{
        async loginUser(){
            try{
                const response = await axios.post('http://127.0.0.1:5000/api/login',{
                    username:this.username,
                    password:this.password,
                });
                const {access_token,user} = response.data;
                console.log(user)
                localStorage.setItem('user',JSON.stringify(user));
                localStorage.setItem('access_token',access_token);

                if (user.role === 'admin'){
                    this.$router.push('/admin-dashboard')
                } else if (user.role === 'store-manager'){ 
                    this.$router.push('store_manager_dashboard')
                } else {
                    this.$router.push('/user_dashboard')
                }
            } catch(error){
                this.errorMessage = error.response ? error.response.data.message:'Login Failed.please try again'
            }
        }
    }
}
</script>


<style scoped>


</style>