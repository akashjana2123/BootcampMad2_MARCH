<template>
    <button @click="exportcsv">Download Report</button>
</template>

<script>
import axios from 'axios';
export default{
    methods:{
        exportcsv(){
            const accessToken = localStorage.getItem('access_token');
            const headers = {
                Authorization: `Bearer ${accessToken}`
            }

            axios.post(' http://127.0.0.1:5000/exportcsv/1',{},{headers,responseType:'blob'})
            .then( response => {
                const url = window.URL.createObjectURL( new Blob([response.data]));
                const downloadLink = document.createElement('a')
                downloadLink.href=url;
                downloadLink.setAttribute('download','category_report.csv');
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            }
            )
            .catch(error =>{
                console.error(error);
            })
        }
    }
}
</script>