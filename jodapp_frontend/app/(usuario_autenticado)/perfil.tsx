// app/(usuario_autenticado)/perfil.tsx
import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput, Modal, Button, ActivityIndicator, StatusBar, } from 'react-native';

import { useAuth } from '@/context/AuthContext';
import VerificationModal from '@/components/VerificationModal';
import TicketsList from '@/components/TicketsList';
import { showMessage } from "react-native-flash-message";
import DateTimePicker from '@react-native-community/datetimepicker';
import { format } from 'date-fns';

// Interfaz para el formulario de cambio de contraseña
interface PasswordForm {
    oldPassword: string;
    newPassword: string;
    confirmPassword: string;
}

export default function ProfileScreen() {
    const { user, cliente, logout, updateProfile, changePassword } = useAuth();
    //const [showVerificationModal, setShowVerificationModal] = useState(false);
    //const [currentTicket, setCurrentTicket] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [editedData, setEditedData] = useState({
        email: user?.email || '',
        nombre: cliente?.nombre || '',
        apellido: cliente?.apellido || '',
        dni: cliente?.dni || '',
        cuil: cliente?.cuil || '',
        fecha_nacimiento: cliente?.fecha_nacimiento || '',
        //fecha_nacimiento: cliente?.fecha_nacimiento ? new Date(cliente.fecha_nacimiento) : new Date(),
    });
    const [showPicker, setShowPicker] = useState(false);

    const onDateChange = (event, selectedDate) => {
        const currentDate = selectedDate || editedData.fecha_nacimiento;
        setShowPicker(false);
        // local time zone
        const localDate = new Date(currentDate);
        localDate.setMinutes(localDate.getMinutes() + localDate.getTimezoneOffset());
        const formatDate = format(localDate, 'yyyy-MM-dd');
        setEditedData(prev => ({ ...prev, fecha_nacimiento: formatDate }));
    };


    // Estado para el modal de cambio de contraseña
    const [showPasswordModal, setShowPasswordModal] = useState(false);
    const [passwordForm, setPasswordForm] = useState<PasswordForm>({
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
    });

    const [isLoading, setIsLoading] = useState(false);
    const handleLogout = async () => {
        try {
            setIsLoading(true);
            // Esperar 2 segundos antes de ejecutar el logout
            await new Promise(resolve => setTimeout(resolve, 2000));
            await logout();
        } catch (error) {
            console.error('Error al cerrar sesión:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleSave = async () => {
        try {
            await updateProfile(editedData);
            showMessage({
                message: "¡Éxito!",
                description: "Perfil actualizado correctamente",
                type: "success",
                duration: 3000,
                floating: true,
            });
            setIsEditing(false);
        } catch (error) {
            showMessage({
                message: "Error",
                description: error instanceof Error ? error.message : "No se pudo actualizar el perfil",
                type: "danger",
                duration: 3000,
                floating: true,
            });
        }
    };

    const handleChangePassword = async () => {
        if (passwordForm.newPassword !== passwordForm.confirmPassword) {
            showMessage({
                message: "Error",
                description: "Las contraseñas no coinciden",
                type: "danger",
                duration: 3000,
                floating: true,
            });
            return;
        }

        try {
            await changePassword(passwordForm.oldPassword, passwordForm.newPassword);
            showMessage({
                message: "¡Éxito!",
                description: "Contraseña actualizada correctamente",
                type: "success",
                duration: 3000,
                floating: true,
            });
            setShowPasswordModal(false);
            setPasswordForm({
                oldPassword: '',
                newPassword: '',
                confirmPassword: '',
            });
        } catch (error) {
            showMessage({
                message: "Error",
                description: error instanceof Error ? error.message : "No se pudo cambiar la contraseña",
                type: "danger",
                duration: 3000,
                floating: true,
            });
        }
    };

    return (
        <View style={styles.container}>
            <StatusBar barStyle="light-content" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>{user?.username || 'Usuario'}</Text>
            </View>
            

            <View style={styles.section}>
                <View style={styles.sectionHeader}>
                    <Text style={styles.sectionTitle}>Perfil</Text>
                    <TouchableOpacity
                        style={styles.changePasswordButton}
                        onPress={() => setShowPasswordModal(true)}
                    >
                        <Text style={styles.changePasswordButtonText}>Cambiar Contraseña</Text>
                    </TouchableOpacity>
                    {!isEditing ? (
                        <TouchableOpacity onPress={handleEdit} style={styles.editButton}>
                            <Text style={styles.editButtonText}>Editar</Text>
                        </TouchableOpacity>
                    ) : (
                        <TouchableOpacity onPress={handleSave} style={styles.saveButton}>
                            <Text style={styles.saveButtonText}>Confirmar</Text>
                        </TouchableOpacity>
                    )}
                </View>

                <View style={styles.infoCard}>
                    <View style={styles.infoField}>
                        <Text style={styles.infoLabel}>Email</Text>
                        {isEditing ? (
                            <TextInput
                                style={styles.input}
                                value={editedData.email}
                                onChangeText={(text) =>
                                    setEditedData(prev => ({ ...prev, email: text }))
                                }
                                placeholder="Ingrese email"
                                placeholderTextColor="#666"
                                autoCorrect={false}
                                autoCapitalize="none"
                                keyboardType='email-address'
                            />
                        ) : (
                            <Text style={styles.infoValue}>{user?.email || 'N/A'}</Text>
                        )}
                    </View>

                    <View style={styles.infoField}>
                        <Text style={styles.infoLabel}>Nombre</Text>
                        {isEditing ? (
                            <TextInput
                                style={styles.input}
                                value={editedData.nombre}
                                onChangeText={(text) =>
                                    setEditedData(prev => ({ ...prev, nombre: text }))
                                }
                                placeholder="Ingrese nombre"
                                placeholderTextColor="#666"
                            />
                        ) : (
                            <Text style={styles.infoValue}>{cliente?.nombre || 'N/A'}</Text>
                        )}
                    </View>

                    <View style={styles.infoField}>
                        <Text style={styles.infoLabel}>Apellido</Text>
                        {isEditing ? (
                            <TextInput
                                style={styles.input}
                                value={editedData.apellido}
                                onChangeText={(text) =>
                                    setEditedData(prev => ({ ...prev, apellido: text }))
                                }
                                placeholder="Ingrese apellido"
                                placeholderTextColor="#666"
                            />
                        ) : (
                            <Text style={styles.infoValue}>{cliente?.apellido || 'N/A'}</Text>
                        )}
                    </View>

                    {/* Repite lo anterior para DNI, CUIL y Fecha de Nacimiento */}
                    <View style={styles.infoField}>
                        <Text style={styles.infoLabel}>DNI</Text>
                        {isEditing ? (
                            <TextInput
                                style={styles.input}
                                value={editedData.dni}
                                onChangeText={(text) =>
                                    setEditedData(prev => ({ ...prev, dni: text }))
                                }
                                placeholder="Ingrese su DNI"
                                placeholderTextColor="#666"
                                keyboardType='number-pad'
                            />
                        ) : (
                            <Text style={styles.infoValue}>{cliente?.dni || 'N/A'}</Text>
                        )}
                    </View>
                    <View style={styles.infoField}>
                        <Text style={styles.infoLabel}>CUIL</Text>
                        {isEditing ? (
                            <TextInput
                                style={styles.input}
                                value={editedData.cuil}
                                onChangeText={(text) =>
                                    setEditedData(prev => ({ ...prev, cuil: text }))
                                }
                                placeholder="Ingrese su CUIL"
                                placeholderTextColor="#666"
                                keyboardType='number-pad'
                            />
                        ) : (
                            <Text style={styles.infoValue}>{cliente?.cuil || 'N/A'}</Text>
                        )}
                    </View>

                    <View style={styles.infoField}>
                        <Text style={styles.infoLabel}>Fecha de Nacimiento</Text>
                        {isEditing ? (
                            <>
                                <Button title="Seleccionar Fecha" onPress={() => setShowPicker(true)} />
                                {showPicker && (
                                    <DateTimePicker
                                        value={new Date(editedData.fecha_nacimiento)} 
                                        mode="date"
                                        display="default"
                                        onChange={onDateChange}
                                    />
                                )}
                            </>
                        ) : (
                                <Text style={styles.infoValue}>{cliente?.fecha_nacimiento ? format(new Date(cliente.fecha_nacimiento), 'yyyy-MM-dd') : 'N/A'}</Text>
                        )}
                    </View>

                </View>

                <TouchableOpacity
                    style={styles.logoutButton}
                    onPress={handleLogout}
                    disabled={isLoading}
                >
                    {isLoading ? (
                        <ActivityIndicator color="#FFFFFF" />
                    ) : (
                        <Text style={styles.logoutButtonText}>Cerrar Sesión</Text>
                    )}
                </TouchableOpacity>
            </View>

            {/* Modal para cambio de contraseña */}
            <Modal
                visible={showPasswordModal}
                transparent={true}
                animationType="slide"
            >
                <View style={styles.modalContainer}>
                    <View style={styles.modalContent}>
                        <Text style={styles.modalTitle}>Cambiar Contraseña</Text>

                        <TextInput
                            style={styles.modalInput}
                            placeholder="Contraseña actual"
                            placeholderTextColor="#666"
                            secureTextEntry
                            value={passwordForm.oldPassword}
                            onChangeText={(text) =>
                                setPasswordForm(prev => ({ ...prev, oldPassword: text }))
                            }
                        />

                        <TextInput
                            style={styles.modalInput}
                            placeholder="Nueva contraseña"
                            placeholderTextColor="#666"
                            secureTextEntry
                            value={passwordForm.newPassword}
                            onChangeText={(text) =>
                                setPasswordForm(prev => ({ ...prev, newPassword: text }))
                            }
                        />

                        <TextInput
                            style={styles.modalInput}
                            placeholder="Confirmar nueva contraseña"
                            placeholderTextColor="#666"
                            secureTextEntry
                            value={passwordForm.confirmPassword}
                            onChangeText={(text) =>
                                setPasswordForm(prev => ({ ...prev, confirmPassword: text }))
                            }
                        />

                        <View style={styles.modalButtons}>
                            <TouchableOpacity
                                style={styles.modalCancelButton}
                                onPress={() => setShowPasswordModal(false)}
                            >
                                <Text style={styles.modalButtonText}>Cancelar</Text>
                            </TouchableOpacity>

                            <TouchableOpacity
                                style={styles.modalConfirmButton}
                                onPress={handleChangePassword}
                            >
                                <Text style={styles.modalButtonText}>Confirmar</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            </Modal>

            
            {/*
            <VerificationModal
                visible={showVerificationModal}
                onClose={() => {
                    setShowVerificationModal(false);
                    setCurrentTicket(null);
                }}
                onVerify={handleVerifyTicket}
                ticketInfo={currentTicket}
            />*/}
        </View>
    );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
    },
  container_2: {
    flexGrow: 1,
    },
  datePicker: {
        width:20,// Ajusta el ancho según sea necesario
        marginTop: 10,
        marginBottom: 10,
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 5,
        padding: 10,
        backgroundColor: '#fff', // Fondo blanco para el DatePicker
  },
  header: {
      height: 80,
      backgroundColor: '#7C03D6',
      justifyContent: 'flex-end',
      paddingBottom: 10,
      paddingHorizontal: 20,
  },
  headerTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
  },
  username: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginTop: 10,
    marginBottom: 0,
  },
  section: {
    padding: 16,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  infoCard: {
    backgroundColor: '#373736',
    padding: 16,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  infoField: {
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  infoLabel: {
    fontSize: 13,
    color: 'white',
    marginBottom: 4,
  },
  infoValue: {
    fontSize: 15,
    color: 'white',
    fontWeight: '500',
  },
  input: {
    backgroundColor: 'white',
    borderRadius: 4,
    padding: 8,
    color: 'black',
    fontSize: 15,
  },
  editButton: {
    backgroundColor: '#B57EDC',
    padding: 8,
    borderRadius: 4,
  },
  editButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '500',
  },
  saveButton: {
    backgroundColor: '#4CAF50',
    padding: 8,
    borderRadius: 4,
  },
  saveButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '500',
  },
  changePasswordButton: {
    backgroundColor: '#B57EDC',
    padding: 8,
    borderRadius: 4,
  },
  changePasswordButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '500',
  },
  logoutButton: {
    height: 40,
    width: 200,
      backgroundColor: '#B57EDC',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 5,
    marginTop: 10,
    marginLeft: 75,
  },
  logoutButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  modalContainer: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: 'white',
    borderRadius: 8,
    padding: 20,
    width: '90%',
    maxWidth: 400,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: 'black',
    textAlign: 'center',
  },
  modalInput: {
    backgroundColor: '#f5f5f5',
    borderRadius: 4,
    padding: 12,
    marginBottom: 12,
    color: 'black',
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 16,
  },
  modalCancelButton: {
    backgroundColor: '#ff4444',
    padding: 12,
    borderRadius: 4,
    flex: 1,
    marginRight: 8,
    alignItems: 'center',
  },
  modalConfirmButton: {
    backgroundColor: '#4CAF50',
    padding: 12,
    borderRadius: 4,
    flex: 1,
    marginLeft: 8,
    alignItems: 'center',
  },
  modalButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '500',
  },
});
