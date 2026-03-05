import { createRouter, createWebHistory } from "vue-router";
import ChannelsView from '../views/ChannelsView.vue';
import GroupsView from "@/views/GroupsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: "/",
        name: "ChannelsView",
        component: ChannelsView
    },
    {
        path: "/groups",
        name: "GroupsView",
        component: GroupsView
    }
  ]
});

export default router;