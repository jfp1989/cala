<template>
    <v-container>
        <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
                <v-card>
                    <v-card-text>
                        <v-container>
                            <v-layout row justify-center>
                                <v-card-title><h2>Iniciar Sesión</h2></v-card-title>  
                            </v-layout>                                             
                            <form @submit.prevent="onLogin">
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                        name="user"
                                        label="Usuario"
                                        id="user"
                                        v-model="user"
                                        type="text"
                                        required
                                        ></v-text-field>   
                                    </v-flex>
                                </v-layout>
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                        name="password"
                                        label="Contraseña"
                                        id="password"
                                        v-model="pass"
                                        type="password"
                                        required
                                        ></v-text-field>   
                                    </v-flex>
                                </v-layout>
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-btn color="primary" type="submit">Ingresar</v-btn>
                                    </v-flex>
                                </v-layout>
                            </form>
                        </v-container>
                    </v-card-text>
                </v-card>
                <v-layout row>
                    <v-flex xs12>
                        <v-text-field
                        name="answer"
                        label="answer"
                        id="answer"
                        v-model="answer.session"
                        type="text"
                        ></v-text-field>   
                    </v-flex>
                </v-layout>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import axios from 'axios';

    export default {
        data(){
            return {
                user: 'sebita',
                pass: 'Pose',
                json: {
                    username: '',
                    password: ''
                },
                answer: {
                    message: '',
                    session: ''
                }
            }
        },
        methods: {
            onLogin(){
                this.json.username = this.user;
                this.json.password = this.pass;
                console.log({user: this.user, password: this.pass})
                axios.post(`http://127.0.0.1:5000/login`, this.json)
                .then(response => {
                // JSON responses are automatically parsed.
                this.answer = response.data;    
                })
                .catch(e => {
                this.errors.push(e)
                    });
            }
        }
    }
</script>
