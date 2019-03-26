<template>
    <v-layout align-start>
        <v-flex>
             <div>
                <v-toolbar flat color="white">
                <v-toolbar-title>Personas</v-toolbar-title>
                <v-divider
                    class="mx-2"
                    inset
                    vertical
                ></v-divider>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="500px">
                    <v-btn slot="activator" color="primary" dark class="mb-2">Nueva Persona</v-btn>
                    <v-card>
                        <v-card-title>
                            <span class="headline">{{ formTitle }}</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container grid-list-md>
                            <v-layout wrap>
                                <v-flex xs12 sm6 md4>
                                <v-text-field v-model="editedItem.name" label="Nombre"></v-text-field>
                                </v-flex>
                                <v-flex xs12 sm6 md4>
                                <v-text-field v-model="editedItem.surname" label="Apellido"></v-text-field>
                                </v-flex>
                                <v-flex xs12 sm6 md4>
                                <v-text-field v-model="editedItem.document" label="Documento"></v-text-field>
                                </v-flex>
                                <v-flex xs12 sm6 md4>
                                <v-text-field v-model="editedItem.nickname" label="Apodo"></v-text-field>
                                </v-flex>
                                <v-flex xs12 sm6 md4>
                                <v-text-field v-model="editedItem.ideology" label="Ideologia"></v-text-field>
                                </v-flex>
                                <v-flex xs12 sm6 md4>
                                <v-text-field v-model="editedItem.ug" label="Ug"></v-text-field>
                                </v-flex>
                            </v-layout>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" flat @click="close">Cancelar</v-btn>
                            <v-btn color="blue darken-1" flat @click="save">Guardar</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                </v-toolbar>
                <v-data-table
                :headers="headers"
                :items="persons"
                class="elevation-1"
                >
                <template slot="items" slot-scope="props">
                    <td>{{ props.item.name }}</td>
                    <td>{{ props.item.surname }}</td>
                    <td>{{ props.item.document }}</td>
                    <td>{{ props.item.nickname }}</td>
                    <td>{{ props.item.ideology }}</td>
                    <td>{{ props.item.ug }}</td>
                    <td class="justify-center layout px-0">
                    <v-icon
                        small
                        class="mr-2"
                        @click="editItem(props.item)"
                    >
                        edit
                    </v-icon>
                    <v-icon
                        small
                        @click="deleteItem(props.item)"
                    >
                        delete
                    </v-icon>
                    </td>
                </template>
                <template slot="no-data">
                    <v-btn color="primary" @click="initialize">Reset</v-btn>
                </template>
                </v-data-table>
            </div>
        </v-flex>
    </v-layout>
</template>
<script>
    import axios from 'axios';

    export default {
        data(){
            return {
                dialog: false,
                headers: [
                    {
                    text: 'Nombre',
                    align: 'left',
                    value: 'name'
                    },
                    { text: 'Apellido', value: 'surname' },
                    { text: 'Documento', value: 'document'},
                    { text: 'Apodo', value: 'nickname' },
                    { text: 'Ideologia', value: 'ideology' },
                    { text: 'Ug', value: 'ug' },
                    { text: 'Acciones', value: 'name', sortable: false, align: 'center'}
                ],
                persons: [],
                editedIndex: -1,
                editedItem: {
                    id: 0,
                    name: '',
                    surname: '',
                    document: 0,
                    nickname: '',
                    ideology: '',
                    ug: 0
                },
                defaultItem: {
                    id: 0,
                    name: '',
                    surname: '',
                    document: 0,
                    nickname: '',
                    ideology: '',
                    ug: 0
                }
            }
        },
        computed: {
            formTitle () {
                return this.editedIndex === -1 ? 'Nueva Persona' : 'Editar Persona'
                }
            },

        watch: {
            dialog (val) {
                val || this.close()
                }
            },

            created () {
            this.initialize()
            },
        methods:{
            initialize () {
                axios.get(`http://127.0.0.1:5000/allPersons`)
                .then(response => {
                // JSON responses are automatically parsed.
                this.persons = response.data;    
                })
                .catch(e => {
                this.errors.push(e)
                })
            },

            editItem (item) {
                this.editedIndex = this.persons.indexOf(item)
                this.editedItem = Object.assign({}, item)
                this.dialog = true
            },

            deleteItem (item) {
                const index = this.persons.indexOf(item)
                this.persons.splice(index, 1)
                axios.delete(`http://127.0.0.1:5000/person/delete/`+Object.assign({}, item).id)
                .catch(e => {
                this.errors.push(e)
                })
            },

            close () {
                this.dialog = false
                setTimeout(() => {
                    this.editedItem = Object.assign({}, this.defaultItem)
                    this.editedIndex = -1
                }, 300)
            },

            save () {
                if (this.editedIndex > -1) {
                    Object.assign(this.persons[this.editedIndex], this.editedItem)
                    axios.put(`http://127.0.0.1:5000/person/edit/`+this.editedItem.id, this.editedItem)
                    .catch(e => {
                    this.errors.push(e)
                    })
                } else {
                    //hay q recargar la pantalla para que este bien el id del usuario creado
                    this.persons.push(this.editedItem)
                    axios.post(`http://127.0.0.1:5000/person/create`, this.editedItem)
                    .catch(e => {
                    this.errors.push(e)
                    });
                } 
                this.close()
            },

            getIdPerson(document){
                axios.get(`http://127.0.0.1:5000/person/`+document)
                    .then(response => {
                    // JSON responses are automatically parsed.
                    return response.data.id
                    })
                    .catch(e => {
                    this.errors.push(e)
                    });
            }
        }
    }   
</script>
