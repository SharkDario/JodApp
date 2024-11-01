//app/(publico)/login.tsx
import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '@/context/AuthContext';
//import AsyncStorage from '@react-native-async-storage/async-storage';
import FlashMessage, { showMessage } from "react-native-flash-message";
//import { loginClient } from '../../services/api';
import { useNavigation } from '@react-navigation/native';

const LoginScreen = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigation = useNavigation();
    const router = useRouter();
    const { login } = useAuth();

    const handleLogin = async () => {
        try {
            await login(username, password);
            /*showMessage({
                message: "¡Bienvenido!",
                description: "Has iniciado sesión exitosamente",
                type: "success",
                icon: "success",
            });*/
        } catch (error: any) {
            showMessage({
                message: "Error",
                description: "Credenciales no válidas",
                type: "danger",
                icon: "danger",
                duration: 3000,
                floating: true,
            });
        }
    };

    return (
        <View style={styles.container}>
            <FlashMessage position="top" />
            <Text style={styles.title}>JodApp</Text>
            <TextInput
                style={styles.input}
                placeholder="* Nombre de usuario"
                placeholderTextColor="#888"
                value={username}
                onChangeText={setUsername}
            />
            <TextInput
                style={styles.input}
                placeholder="* Contraseña"
                placeholderTextColor="#888"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />
            
            <TouchableOpacity
                style={[styles.button]}
                onPress={handleLogin}
            >
                <Text style={styles.buttonText}>Entrar</Text>
            </TouchableOpacity>
            <Text
                style={styles.link}
                onPress={() => router.push('/signup')}
            >
                ¿No tienes una cuenta? Regístrate
            </Text>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 16,
        backgroundColor: '#7C03D6',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 24,
    },
    input: {
        width: '90%',
        height: 40,
        color: 'black',
        borderColor: 'black',
        borderWidth: 1,
        borderRadius: 5,
        marginBottom: 16,
        paddingHorizontal: 8,
        backgroundColor: '#E6E6FA',
    },
    link: {
        marginTop: 16,
        color: 'white',
        textDecorationLine: 'underline',
    },
    button: {
        width: 200,
        height: 40,
        backgroundColor: '#B57EDC',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 5,
        marginBottom: 16,
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
    buttonDisabled: {
        backgroundColor: '#999',
    },
});

export default LoginScreen;