//import AsyncStorage from '@react-native-async-storage/async-storage';

// services/api.tsx 
import axios from 'axios';
import { configURL } from '../config/config';

const baseURL = configURL;


// Tipo para los datos de login del cliente
interface LoginClientData {
    username: string;
    password: string;
}
// Tipo para la respuesta de login
interface LoginResponse {
    access: string;
    refresh: string;
    message: string;
}

export const loginClient = async (
    loginData: LoginClientData
): Promise<LoginResponse> => {
    try {
        const response = await axios.post<LoginResponse>(`${baseURL}/api/modulo_clientes/login/`, loginData);
        return response.data;
    } catch (error: any) {
        throw error.response?.data || { error: 'Error desconocido' };
    }
};

// Tipo para los datos de registro del cliente
interface RegisterClientData {
    username: string;
    password: string;
    email: string;
    dni: string;
    cuil: string;
    nombre: string;
    apellido: string;
    fecha_nacimiento: Date; // Formato: 'YYYY-MM-DD'
}

// Tipo para la respuesta de registro
interface RegisterResponse {
    message: string;
}

export const registerClient = async (
    clientData: RegisterClientData
): Promise<RegisterResponse> => {
    try {
        const response = await axios.post<RegisterResponse>(`${baseURL}/api/modulo_clientes/registrar/`, clientData);
        return response.data;
   } catch (error: any) {
        throw error.response?.data || { error: 'Error desconocido' };
    }
};
