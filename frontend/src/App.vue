<template>
  <v-app id="inspire">
    <v-toolbar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      color="blue darken-3"
      dark
      app
      fixed
    >
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <span>Kala</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn 
        flat
        v-for="item in menuItem" 
        :key="item.title"
        router
        :to="item.link"
        >
          <v-icon left dark>{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-slide-y-transition mode="out-in">
          <router-view/>
        </v-slide-y-transition>
      </v-container>
    </v-content>
  </v-app>
</template>


<script>
  export default {
    name: 'App',
    data () {
      return {
        menuItem: [
          {icon: 'home', title: 'Inicio', link: '/'},
          {icon: 'accessibility_new', title: 'Personas', link: '/persons'},
          {icon: 'perm_identity', title: 'Iniciar Sesion', link: '/login'},
        ]
      }
    }
  }
</script>
