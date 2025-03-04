<template>
    <div>
        <h2>
            Signup
        </h2>
        <form @submit.prevent="signupUser">
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div>
                <label for="email">Email:</label>
                <input type="text" id="email" v-model="email" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <div>
                <input type="radio" id="user" value="user" v-model="role" required>
                <label for="user">User</label>
                <input type="radio" id="store-manager" value="store-manager" v-model="role" required>
                <label for="store-manager">Store Manager</label>
            </div>
            <button type="submit">Signup</button>
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
            email:'',
            password:'',
            role:'user',
            errorMessage:''
        }
    },
    methods:{
        async signupUser(){
            try{
                await axios.post('http://127.0.0.1:5000/api/signup',{
                    username:this.username,
                    email:this.email,
                    password:this.password,
                    role:this.role
                });
                this.$router.push('/login')
            } catch(error){
                this.errorMessage = error.response ? error.response.data.message:'Signup Failed.please try again'
            }
        }
    }
}
</script>


<style scoped>


</style>