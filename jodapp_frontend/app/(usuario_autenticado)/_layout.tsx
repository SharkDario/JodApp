// app/(usuario_autenticado)/_layout.tsx (Layout para usuarios autenticados)
import { Drawer } from 'expo-router/drawer';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createMaterialBottomTabNavigator } from '@react-navigation/material-bottom-tabs';
import { useColorScheme } from '@/hooks/useColorScheme';
import { Colors } from '@/constants/Colors';
import { TabBarIcon } from '@/components/navigation/TabBarIcon';
import { useAuth } from '@/context/AuthContext';
import { useEffect } from 'react';
import { router } from 'expo-router';

import DashboardScreen from './index';
import EntradasScreen from './entradas';
import MesasScreen from './mesas';
import BarScreen from './bar';
import ProfileScreen from './perfil';
import TicketsScreen from './tickets';
import { fontConfig } from 'react-native-paper/lib/typescript/styles/fonts';
import Ionicons from '@expo/vector-icons/Ionicons';
import Entypo from '@expo/vector-icons/Entypo';
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import MaterialCommunityIcons from '@expo/vector-icons/MaterialCommunityIcons';
import Fontisto from '@expo/vector-icons/Fontisto';

export default function AuthenticatedLayout() {
  const colorScheme = useColorScheme();
  const { isAuthenticated, logout, refreshAuth } = useAuth();
  const Tab = createMaterialBottomTabNavigator();

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/(publico)/login');
    }
  }, [isAuthenticated]);

    // Common listener configuration for all tabs
    const getTabListeners = (screenName: string) => ({
        tabPress: () => {
            console.log(`${screenName} tab pressed - refreshing auth`);
            refreshAuth();
        },
    });
  //<MaterialIcons name="nights-stay" size={24} color={color} />
    //<MaterialIcons name="dark-mode" size={24} color={color} /> <MaterialCommunityIcons name="party-popper" size={24} color={color} />
  return (
    <Tab.Navigator
      initialRouteName="JodApp"
      activeColor= 'black'
      inactiveColor= 'white'
      shifting
      barStyle={{
        backgroundColor: '#7C03D6',
        height: 60,
      }}
    >
      <Tab.Screen
        name="JodApp"
        component={DashboardScreen}
        options={{
          tabBarLabel: '',
          tabBarIcon: ({ color }) => (
            <Fontisto name="map-marker-alt" size={24} color={color} />
            ),
        }}
        listeners={getTabListeners('JodApp')}
      />
      <Tab.Screen
        name="Entradas"
        component={EntradasScreen}
        options={{
          tabBarLabel: '',
          tabBarIcon: ({ color }) => (
            <Entypo name="ticket" color={color} size={24} />
          ),
        }}
        listeners={getTabListeners('Entradas')}
      />
      <Tab.Screen
        name="Mesas"
        component={MesasScreen}
        options={{
          tabBarLabel: '',
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="table-bar" color={color} size={24} />
          ),
        }}
        listeners={getTabListeners('Mesas')}
      />
      <Tab.Screen
        name="Bar"
        component={BarScreen}
        options={{
          tabBarLabel: '',
          tabBarIcon: ({ color }) => (
            <Entypo name="drink" color={color} size={24} />
          ),
        }}
        listeners={getTabListeners('Bebidas')}
          />
          <Tab.Screen
              name="Tickets"
              component={TicketsScreen}
              options={{
                  tabBarLabel: '',
                  tabBarIcon: ({ color }) => (
                      <Ionicons name="ticket" color={color} size={24} />
                  ),
              }}
              listeners={getTabListeners('Tickets')}
          />
      <Tab.Screen
        name="Perfil"
        component={ProfileScreen}
        options={{
          tabBarLabel: '',
          tabBarIcon: ({ color }) => (
            <Ionicons name="person" color={color} size={24} />
          ),
        }}
        listeners={getTabListeners('Perfil')}
      />
      
    </Tab.Navigator>
    
  );
}
/*
<Drawer
      screenOptions={{
        drawerActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        drawerInactiveTintColor: colorScheme === 'dark' ? '#fff' : '#000',
        drawerStyle: {
          backgroundColor: Colors[colorScheme ?? 'light'].background,
        },
        headerStyle: {
          backgroundColor: Colors[colorScheme ?? 'light'].background,
        },
        headerTintColor: colorScheme === 'dark' ? '#fff' : '#000',
      }}
    >
      <Drawer.Screen
        name="index"
        options={{
          title: 'JodApp',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'home' : 'home-outline'} color={color} size={size} />
          ),
        }}
      />
      <Drawer.Screen
        name="perfil"
        options={{
          title: 'Mi Perfil',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'person' : 'person-outline'} color={color} size={size} />
          ),
        }}
      />
    </Drawer>

import { Redirect } from 'expo-router';
import { Drawer } from 'expo-router/drawer';
import { useColorScheme } from '@/hooks/useColorScheme';
import { Colors } from '@/constants/Colors';
import { TabBarIcon } from '@/components/navigation/TabBarIcon';
import { useAuth } from '@/context/AuthContext';

export default function AuthenticatedLayout() {
  const colorScheme = useColorScheme();
  const { isAuthenticated, logout } = useAuth();

  // Si no está autenticado, redirige al login
  if (!isAuthenticated) {
    return <Redirect href="/login" />;
  }

  return (
    <Drawer
      screenOptions={{
        drawerActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        // ... resto de opciones del drawer
      }}
    >
      <Drawer.Screen
        name="index" // será /usuario_autenticado/index
        options={{
          title: 'Dashboard',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'home' : 'home-outline'} color={color} size={size} />
          ),
        }}
      />
      <Drawer.Screen
        name="perfil" // será /usuario_autenticado/perfil
        options={{
          title: 'Mi Perfil',
          drawerIcon: ({ color, size, focused }) => (
            <TabBarIcon name={focused ? 'person' : 'person-outline'} color={color} size={size} />
          ),
        }}
      />
      {/* Más pantallas para usuarios autenticados /}
    </Drawer>
  );
}*/