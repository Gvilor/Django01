import { createRouter, createWebHistory } from "vue-router";
import ChannelsView from "@/views/ChannelsView.vue";
import GroupsView from "@/views/GroupsView.vue";
import ChannelTypesView from "@/views/ChannelTypesView.vue";
import DescriptionsView from "@/views/DescriptionsView.vue";
import SubscribersView from "@/views/SubscribersView.vue";

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
    },
    {
      path: "/channel-types",
      name: "channel-types",
      component: ChannelTypesView,
    },
    {
      path: "/descriptions",
      name: "descriptions",
      component: DescriptionsView,
    },
    {
      path: "/subscribers",
      name: "subscribers",
      component: SubscribersView,
    },
  ]
});

export default router;