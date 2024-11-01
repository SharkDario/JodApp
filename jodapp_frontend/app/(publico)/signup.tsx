// app/signup.tsx
import React, { useState } from 'react';
import { Text, TextInput, Button, Alert, StyleSheet, ScrollView, TouchableOpacity, Pressable } from 'react-native';
import { useRouter } from 'expo-router';
import DateTimePicker from '@react-native-community/datetimepicker';
import { registerClient } from '../../services/api';
import FlashMessage, { showMessage } from 'react-native-flash-message';

// Tipos para el estado del formulario
interface RegisterFormState {
    username: string;
    password: string;
    email: string;
    dni: string;
    cuil: string;
    nombre: string;
    apellido: string;
    fecha_nacimiento: Date | null;
}

const SignupScreen: React.FC = () => {
    const router = useRouter();

    const [formState, setFormState] = useState<RegisterFormState>({
        username: '',
        password: '',
        email: '',
        dni: '',
        cuil: '',
        nombre: '',
        apellido: '',
        fecha_nacimiento: null,
    });
    const [date, setDate] = useState(new Date());
    const [showDatePicker, setShowDatePicker] = useState(false);

    // Función para manejar cambios en los inputs
    const handleChange = (field: keyof RegisterFormState, value: string | Date) => {
        setFormState({ ...formState, [field]: value });
    };

    // Función para manejar el registro
    const handleRegister = async () => {
        try {
        const formData = {
                ...formState,
                fecha_nacimiento: formState.fecha_nacimiento
                    ? formState.fecha_nacimiento.toISOString().split('T')[0]
                    : '',
        };
        const result = await registerClient(formData);
        showMessage({
            message: "Éxito",
            description: result.message,
            type: "success",
            icon: "success",
            duration: 3000,
            floating: true,
        });
        // Restablecer los campos del formulario
        setFormState({
            username: '',
            password: '',
            email: '',
            dni: '',
            cuil: '',
            nombre: '',
            apellido: '',
            fecha_nacimiento: null,
        });
        } catch (error: any) {
            showMessage({
                message: "Error",
                description: error.error || 'Error al registrar el cliente',
                type: "danger",
                icon: "danger",
                duration: 3000,
                floating: true,
            });
        }
    };

    // Función para mostrar el selector de fecha
    const handleDateChange = (event: any, selectedDate?: Date) => {
        setShowDatePicker(false);
        if (selectedDate) {
            // Configura la fecha para reflejar la zona horaria local
            const localDate = new Date(selectedDate);
            setDate(localDate);
            handleChange('fecha_nacimiento', localDate); // Aquí llamas tu función para guardar la fecha
            //handleChange('fecha_nacimiento', selectedDate);
        }
    };

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <FlashMessage position="top"/> 
            <Text style={styles.title}>JodApp</Text>
            <TextInput
                placeholder="* Nombre de usuario"
                placeholderTextColor="#888"
                value={formState.username}
                onChangeText={(value) => handleChange('username', value)}
                style={styles.input}
            />
            <TextInput
                placeholder="* Contraseña"
                placeholderTextColor="#888"
                value={formState.password}
                onChangeText={(value) => handleChange('password', value)}
                secureTextEntry
                style={styles.input}
            />
            <TextInput
                placeholder="* Correo electrónico"
                placeholderTextColor="#888"
                value={formState.email}
                onChangeText={(value) => handleChange('email', value)}
                style={styles.input}
            />
            <TextInput
                placeholder="* DNI"
                placeholderTextColor="#888"
                value={formState.dni}
                onChangeText={(value) => handleChange('dni', value)}
                keyboardType="numeric"
                maxLength={10}
                style={styles.input}
            />
            <TextInput
                placeholder="* CUIL"
                placeholderTextColor="#888"
                value={formState.cuil}
                onChangeText={(value) => handleChange('cuil', value)}
                keyboardType="numeric"
                maxLength={15}
                style={styles.input}
            />
            <TouchableOpacity onPress={() => setShowDatePicker(true)} style={styles.button_2}>
                <Text style={{ color: formState.fecha_nacimiento ? 'white' : 'white' }}>
                    {formState.fecha_nacimiento
                        ? formState.fecha_nacimiento.toISOString().split('T')[0]
                        : '* Fecha de nacimiento 🗓️'}
                </Text>
            </TouchableOpacity>
            {showDatePicker && (
                <DateTimePicker
                    value={formState.fecha_nacimiento || new Date()}
                    mode="date"
                    display="default"
                    onChange={handleDateChange}
                    timeZoneOffsetInMinutes={0} // Asegura el uso de la zona horaria local
                    themeVariant="dark"
                />
            )}
            <TextInput
                placeholder="* Nombre"
                placeholderTextColor="#888"
                value={formState.nombre}
                onChangeText={(value) => handleChange('nombre', value)}
                style={styles.input}
            />
            <TextInput
                placeholder="* Apellido"
                placeholderTextColor="#888"
                value={formState.apellido}
                onChangeText={(value) => handleChange('apellido', value)}
                style={styles.input}
            />
            

            <TouchableOpacity style={styles.button} onPress={handleRegister}>
                <Text style={styles.buttonText}>Registrarte</Text>
            </TouchableOpacity>
            <Text style={styles.link} onPress={() => router.push('/login')}>
                ¿Tienes una cuenta? Entrar
            </Text>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flexGrow: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#7C03D6',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        marginBottom: 24,
        textAlign: 'center',
    },
    input: {
        //padding: 10,
        //marginVertical: 10,
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
    button_2: {
        width: '90%',
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
});

export default SignupScreen;
