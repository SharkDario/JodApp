// context/AuthContext.tsx
import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { loginClient } from '../services/api';
import { configURL } from '../config/config';
import { router } from 'expo-router';
import FlashMessage, { showMessage } from "react-native-flash-message";
import { Linking } from 'react-native';
import axios from 'axios';

const baseURL = configURL;

interface Cliente {
    id: number;
    nombre: string;
    apellido: string;
    dni: string;
    cuil: string;
    fecha_nacimiento: string;
    embedding: string | null;
    foto: string | null;
    // Add stats properties
    total_reservaciones: number | 0;
    racha_actual: number | 0;
    total_productos: number | 0;
    total_entradas: number | 0;
}

interface User {
    id: number;
    username: string;
    email: string;
}

interface Mesa {
    id: number;
    categoria: string;
    capacidad: number;
    precio: number;
    disponibilidad: boolean;
    posicion: { top: number; left: number };
    color: string;
    numero: number;
}

interface Entrada {
    id: number;
    categoria: string;
    precio_unitario: number;
}

interface Fiesta {
    id: number;
    fecha: string;
    nombre: string;
    descripcion: string;
    edad_minima: number;
    edad_maxima: number;
    latitud: number;
    longitud: number;
    cantidad_entrada_vip: number;
    cantidad_entrada_popular: number;
    categoria: string;
    vestimenta: string;
    mesas: Mesa[];
    entradas: Entrada[];
}

interface Producto {
    id: number;
    nombre: string;
    volumen: number;  // Volumen en mililitros
    precio_unitario: number;  // Precio por unidad
    stock: number;  // Cantidad en stock
    stock_minimo: number;  // Cantidad mínima en stock
    marca: string;  // Marca del producto
}

interface Trago {
    id: number;
    nombre: string;
    volumen: number;  // Volumen en mililitros
    precio_unitario: number;  // Precio por unidad
    stock: number;  // Cantidad en stock
    stock_minimo: number;  // Cantidad mínima en stock
    tipo: string;  // Tipo de trago, como "Cóctel", "Shot", "Licuado"
}

interface Ticket {
    id: number;
    tipo: 'articulo' | 'entrada';
    nombre?: string;
    fiesta?: string;
    categoria?: string;
    cantidad: number;
}

interface TicketsResponse {
    articulos: Ticket[];
    entradas: Ticket[];
    success?: boolean;
    mensaje?: string;
}

interface AuthContextType {
    isAuthenticated: boolean;
    user: User | null;
    cliente: Cliente | null;
    login: (username: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    updateProfile: (data: Partial<UpdateProfileData>) => Promise<void>;
    changePassword: (oldPassword: string, newPassword: string) => Promise<void>;
    refreshAuth: () => Promise<void>;
    reservarMesa: (mesaId: number) => Promise<void>;
    comprarEntradas: (entradaId: number, cantidad: number, fiestaId: number) => Promise<void>;
    comprarCarrito: (purchaseData: any) => Promise<void>;
    loadTickets: () => Promise<void>;
    confirmarCanje: (ticketId: number, tipo: string, codigo: string) => Promise<void>;
    isLoading: boolean;
    accessToken: string | null;
    refreshToken: string | null;
    fiestas: {
        viernes: Fiesta[];
        sabado: Fiesta[];
    } | null;
    tickets: TicketsResponse | null;
    tragos: Trago[] | null;
    productos: Producto[] | null;
}

interface UpdateProfileData {
    email: string;
    nombre: string;
    apellido: string;
    dni: string;
    cuil: string;
    fecha_nacimiento: string;
}

interface MesaReservada {
    id: number;
    mesa_id: number;
    categoria: string;
    capacidad: number;
    numero: number;
}

const AuthContext = createContext<AuthContextType>({
    isAuthenticated: false,
    user: null,
    cliente: null,
    login: async () => {},
    logout: async () => {},
    updateProfile: async () => { },
    refreshAuth: async () => { },
    changePassword: async () => { },
    reservarMesa: async () => { },
    comprarEntradas: async () => { },
    comprarCarrito: async () => { },
    loadTickets: async () => { },
    confirmarCanje: async () => { },
    isLoading: true,
    accessToken: null,
    refreshToken: null,
    fiestas: null,
    tickets: null,
    tragos: null,
    productos: null,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState<User | null>(null);
    const [cliente, setCliente] = useState<Cliente | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [refreshToken, setRefreshToken] = useState<string | null>(null);
    const [fiestas, setFiestas] = useState<{
        viernes: Fiesta[];
        sabado: Fiesta[];
    } | null>(null);
    const [tragos, setTragos] = useState<Trago[] | null>(null);
    const [productos, setProductos] = useState<Producto[] | null>(null);
    const [tickets, setTickets] = useState<TicketsResponse>({
        articulos: [],
        entradas: []
    });

    useEffect(() => {
        checkAuth();
    }, []);

    const loadTickets = useCallback(async () => {
        try {
            //if (!accessToken) {
            //    throw new Error('No hay token de acceso');
            //}
            //if (!cliente?.id) {
            //    throw new Error('No hay cliente identificado');
            //}

            const response = await api.get<TicketsResponse>(
                `/api/modulo_clientes/obtener-tickets-cliente/${cliente.id}/`
            );
            setTickets(response.data);
        } catch (error) {
            //console.error('Error al cargar tickets:', error);
            if (axios.isAxiosError(error)) {
                const errorMessage = error.response?.data?.error || "No se pudieron cargar los tickets";
                //showMessage({
                //    message: "Error",
                //    description: errorMessage,
                //    type: "danger",
                //    duration: 3000,
                //    floating: true,
                //});
            }
            //throw error;
        }
    }, [accessToken, cliente?.id]);
    
    const confirmarCanje = useCallback(async (ticketId: number, tipo: string, codigo: string) => {
        try {
            if (!accessToken) {
                throw new Error('No hay token de acceso');
            }
            if (!cliente?.id) {
                throw new Error('No hay cliente identificado');
            }

            const response = await api.post<{ success: boolean; mensaje: string }>(
                '/api/modulo_clientes/confirmar-canje-cliente/',
                {
                    ticket_id: ticketId,
                    tipo: tipo,
                    codigo: codigo,
                    cliente_id: cliente.id
                }
            );

            if (response.data.success) {
                await loadTickets();
                showMessage({
                    message: "¡Éxito!",
                    description: response.data.mensaje,
                    type: "success",
                    duration: 3000,
                    floating: true,
                });
            }
        } catch (error) {
            console.error('Error al confirmar canje:', error);
            if (axios.isAxiosError(error)) {
                const errorMessage = error.response?.data?.error || "Error al confirmar el canje";
                showMessage({
                    message: "Error",
                    description: errorMessage,
                    type: "danger",
                    duration: 3000,
                    floating: true,
                });
                throw new Error(errorMessage);
            }
            throw error;
        }
    }, [accessToken, cliente?.id, loadTickets]);
    
    const refreshAuth = async () => {
        try {
            setIsLoading(true);
            const storedAccessToken = await AsyncStorage.getItem('accessToken');

            if (!storedAccessToken) {
                setIsAuthenticated(false);
                router.replace('/(publico)/login');
                return;
            }

            // Crear una instancia temporal de axios con el token actual
            const tempApi = axios.create({
                baseURL,
                headers: {
                    Authorization: `Bearer ${storedAccessToken}`
                }
            });

            // Hacer una petición para obtener los datos actualizados
            const response = await tempApi.get('/api/modulo_clientes/refresh-data/');

            // Actualizar los datos en el estado y en AsyncStorage
            const updatedData = response.data;

            // Actualizar user y cliente
            setUser(updatedData.user);
            setCliente({
                ...updatedData.cliente,
                embedding: updatedData.cliente.embedding || null,
                foto: updatedData.cliente.foto || null
            });

            // Actualizar fiestas
            const updatedFiestas = {
                viernes: updatedData.fiestas_viernes || [],
                sabado: updatedData.fiestas_sabado || [],
            };
            setFiestas(updatedFiestas);

            await loadTickets()

            // Guardar los datos actualizados en AsyncStorage
            await AsyncStorage.setItem('user', JSON.stringify(updatedData.user));
            await AsyncStorage.setItem('cliente', JSON.stringify({
                ...updatedData.cliente,
                embedding: updatedData.cliente.embedding || null,
                foto: updatedData.cliente.foto || null
            }));
            await AsyncStorage.setItem('fiestas', JSON.stringify(updatedFiestas));

            setTragos(updatedData.tragos || []);
            setProductos(updatedData.productos || []);

            // If storing in AsyncStorage as well:
            await AsyncStorage.setItem('tragos', JSON.stringify(updatedData.tragos || []));
            await AsyncStorage.setItem('productos', JSON.stringify(updatedData.productos || []));


            setIsAuthenticated(true);

        } catch (error) {
            console.error('Error. Vuelva a iniciar sesión', error);
            if (axios.isAxiosError(error) && error.response?.status === 401) {
                // Si el token expiró, hacer logout
                await logout();
                //router.replace('/(publico)/login');
            }
        } finally {
            setIsLoading(false);
        }
    };

    const checkAuth = async () => {
        try {
            const storedAccessToken = await AsyncStorage.getItem('accessToken');
            const storedRefreshToken = await AsyncStorage.getItem('refreshToken');
            const storedUser = await AsyncStorage.getItem('user');
            const storedCliente = await AsyncStorage.getItem('cliente');
            const storedFiestas = await AsyncStorage.getItem('fiestas');
            if (storedFiestas) setFiestas(JSON.parse(storedFiestas));

            if (storedAccessToken && storedRefreshToken) {
                setAccessToken(storedAccessToken);
                setRefreshToken(storedRefreshToken);
                if (storedUser) setUser(JSON.parse(storedUser));
                if (storedCliente) setCliente(JSON.parse(storedCliente));
                setIsAuthenticated(true);
                router.replace('/(usuario_autenticado)');
            } else {
                setIsAuthenticated(false);
                router.replace('/(publico)/login');
            }
        } catch (error) {
            console.error(error);
            setIsAuthenticated(false);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (username: string, password: string) => {
        try {
            const response = await loginClient({ username, password });

            // Store tokens
            await AsyncStorage.setItem('accessToken', response.access);
            await AsyncStorage.setItem('refreshToken', response.refresh);
            
            // Store user and client data
            await AsyncStorage.setItem('user', JSON.stringify(response.user));
            await AsyncStorage.setItem('cliente', JSON.stringify({
                ...response.cliente,
                embedding: response.cliente.embedding || null,
                foto: response.cliente.foto || null
            }));

            // Store fiestas data
            await AsyncStorage.setItem('fiestas', JSON.stringify({
                viernes: response.fiestas_viernes,
                sabado: response.fiestas_sabado,
            }));

            // If storing in AsyncStorage as well:
            await AsyncStorage.setItem('tragos', JSON.stringify(response.tragos || []));
            await AsyncStorage.setItem('productos', JSON.stringify(response.productos || []));
            
            // Update state
            setAccessToken(response.access);
            setRefreshToken(response.refresh);
            setUser(response.user);
            setCliente({
                ...response.cliente,
                embedding: response.cliente.embedding || null,
                foto: response.cliente.foto || null
            });
            // Update state
            setFiestas({
                viernes: response.fiestas_viernes || null,
                sabado: response.fiestas_sabado || null,
            });

            setTragos(response.tragos || []);
            setProductos(response.productos || []);

            setIsAuthenticated(true);

            showMessage({
                message: "¡Bienvenid@!",
                description: response.message,
                type: "success",
                icon: "success",
                duration: 3000,
                floating: true,
            });
            router.replace('/(usuario_autenticado)');
        } catch (error) {
            throw error;
        }
    };

    const logout = async () => {
        try {
            await AsyncStorage.multiRemove([
                'accessToken',
                'refreshToken',
                'user',
                'cliente',
                'fiestas',
            ]);
            setFiestas(null);
            setAccessToken(null);
            setRefreshToken(null);
            setUser(null);
            setCliente(null);
            setTickets({
                articulos: [],
                entradas: []
            });
            setIsAuthenticated(false);
            router.replace('/(publico)/login');
        } catch (error) {
            console.error(error);
        }
    };

    // Crear instancia de axios con configuración base
    const api = axios.create({
        baseURL: baseURL, // Cambia esto por tu URL base
    });

    // Interceptor para agregar el token a todas las peticiones
    api.interceptors.request.use(
        (config) => {
            if (accessToken) {
                config.headers.Authorization = `Bearer ${accessToken}`;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    const updateProfile = async (data: Partial<UpdateProfileData>) => {
        try {
            const response = await api.put('/api/modulo_clientes/actualizar-perfil/', data);

            // Actualizar el estado y AsyncStorage
            setUser(response.data.user);
            setCliente(response.data.cliente);
            await AsyncStorage.setItem('user', JSON.stringify(response.data.user));
            await AsyncStorage.setItem('cliente', JSON.stringify(response.data.cliente));

            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.response?.status === 401) {
                    // Token expirado o inválido
                    await logout();
                    //router.replace('/(publico)/login');
                }
                throw new Error(error.response?.data?.error || 'Error al actualizar el perfil');
            }
            throw error;
        }
    };

    const changePassword = async (oldPassword: string, newPassword: string) => {
        try {
            const response = await api.post('/api/modulo_clientes/cambiar-password/', {
                old_password: oldPassword,
                new_password: newPassword,
            });

            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.response?.status === 401) {
                    // Token expirado o inválido
                    await logout();
                    //router.replace('/(publico)/login');
                }
                throw new Error(error.response?.data?.error || 'Error al cambiar la contraseña');
            }
            throw error;
        }
    };

    const reservarMesa = async (mesaId: number) => {
        try {
            if (!cliente || !cliente.id) {
                throw new Error('No hay un cliente autenticado');
            }

            const response = await api.put('/api/modulo_clientes/reservar-mesa/', {
                mesa_id: mesaId,
                cliente_id: cliente.id
            });

            if (response.data.success) {
                // Actualizar el estado local después de una reserva exitosa
                await refreshAuth();

                showMessage({
                    message: "¡Éxito!",
                    description: "Mesa reservada correctamente",
                    type: "success",
                    icon: "success",
                    duration: 3000,
                    floating: true,
                });
                // Verifica si `pago_url` está en la respuesta y redirige al usuario al enlace de pago
                if (response.data.pago_url) {
                    Linking.openURL(response.data.pago_url)
                        .catch(err => {
                            console.error("Failed to open URL: ", err);
                            showMessage({
                                message: "Error",
                                description: "No se pudo abrir el enlace de pago.",
                                type: "danger",
                                icon: "danger",
                                duration: 3000,
                                floating: true,
                            });
                        });
                }
            }

            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const errorMessage = error.response?.data?.error || 'Error al reservar la mesa';
                showMessage({
                    message: "Error",
                    description: errorMessage,
                    type: "danger",
                    icon: "danger",
                    duration: 3000,
                    floating: true,
                });
                throw new Error(errorMessage);
            }
            throw error;
        }
    };

    const comprarEntradas = async (entradaId: number, cantidad: number, fiestaId: number) => {
        try {
            if (!cliente || !cliente.id) {
                throw new Error('No hay un cliente autenticado');
            }

            const response = await api.put('/api/modulo_clientes/comprar-entradas/', {
                entrada_id: entradaId,
                cantidad: cantidad,
                cliente_id: cliente.id,
                fiesta_id: fiestaId
            });

            if (response.data.success) {
                if (response.data.pago_url) {
                    await Linking.openURL(response.data.pago_url);
                }

                showMessage({
                    message: "¡Éxito!",
                    description: "¡Entradas compradas!",
                    type: "success",
                    duration: 3000,
                    floating: true,
                });
            }
            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const errorMessage = error.response?.data?.error || 'Error al comprar las entradas';
                showMessage({
                    message: "Error",
                    description: errorMessage,
                    type: "danger",
                    duration: 3000,
                    floating: true,
                });
                throw new Error(errorMessage);
            }
            throw error;
        }
    };

    const comprarCarrito = async (purchaseData: any) => {
        try {
            if (!cliente || !cliente.id) {
                throw new Error('No hay un cliente autenticado');
            }
            const response = await api.put('/api/modulo_clientes/comprar-carrito/', {
                items: purchaseData.items,
                cliente_id: cliente.id
            });
            if (response.data.success) {
                if (response.data.pago_url) {
                    await Linking.openURL(response.data.pago_url);
                }
                showMessage({
                    message: "¡Éxito!",
                    description: "¡Carrito comprado!",
                    type: "success",
                    duration: 3000,
                    floating: true,
                });
            }
            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const errorMessage = error.response?.data?.error || 'Error al comprar el carrito';
                showMessage({
                    message: "Error",
                    description: errorMessage,
                    type: "danger",
                    duration: 3000,
                    floating: true,
                });
                throw new Error(errorMessage);
            }
            throw error;
        }
    };

    return (
        <AuthContext.Provider value={{
            isAuthenticated,
            user,
            cliente,
            login,
            logout,
            updateProfile,
            changePassword,
            isLoading,
            accessToken,
            refreshToken,
            fiestas,
            refreshAuth,
            tragos,
            productos,
            reservarMesa,
            comprarEntradas,
            comprarCarrito,
            tickets,
            loadTickets,
            confirmarCanje,
        }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);

/*
Para probar después
const refreshAuth = async () => {
    let retryCount = 0;
    const maxRetries = 2;

    const attemptRefresh = async () => {
        try {
            setIsLoading(true);
            const storedAccessToken = await AsyncStorage.getItem('accessToken');
            
            if (!storedAccessToken) {
                setIsAuthenticated(false);
                router.replace('/(publico)/login');
                return;
            }

            const tempApi = axios.create({
                baseURL,
                headers: {
                    Authorization: `Bearer ${storedAccessToken}`
                }
            });

            // Agregamos un timeout a la petición
            const response = await tempApi.get('/api/modulo_clientes/refresh-data/', {
                timeout: 5000 // 5 segundos de timeout
            });
            
            const updatedData = response.data;
            
            // Actualizar estados
            setUser(updatedData.user);
            setCliente({
                ...updatedData.cliente,
                embedding: updatedData.cliente.embedding || null,
                foto: updatedData.cliente.foto || null
            });

            const updatedFiestas = {
                viernes: updatedData.fiestas_viernes || [],
                sabado: updatedData.fiestas_sabado || [],
            };
            setFiestas(updatedFiestas);

            // Actualizar AsyncStorage
            await Promise.all([
                AsyncStorage.setItem('user', JSON.stringify(updatedData.user)),
                AsyncStorage.setItem('cliente', JSON.stringify({
                    ...updatedData.cliente,
                    embedding: updatedData.cliente.embedding || null,
                    foto: updatedData.cliente.foto || null
                })),
                AsyncStorage.setItem('fiestas', JSON.stringify(updatedFiestas))
            ]);

            setIsAuthenticated(true);

        } catch (error) {
            console.error(`Refresh attempt ${retryCount + 1} failed:`, error);
            
            if (axios.isAxiosError(error)) {
                // Si es un error de timeout o de red, intentamos de nuevo
                if (!error.response || error.code === 'ECONNABORTED') {
                    if (retryCount < maxRetries) {
                        retryCount++;
                        console.log(`Retrying refresh... Attempt ${retryCount + 1}`);
                        // Esperar 1 segundo antes de reintentar
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        return attemptRefresh();
                    }
                }
                
                // Si es 401 y ya agotamos los reintentos, hacemos logout
                if (error.response?.status === 401 && retryCount >= maxRetries) {
                    await logout();
                    router.replace('/(publico)/login');
                }
            }
        } finally {
            setIsLoading(false);
        }
    };

    return attemptRefresh();
};
*/