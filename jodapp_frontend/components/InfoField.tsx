import React, { useState } from 'react';
import { View, TextInput, Text, StyleSheet } from 'react-native';

interface InfoFieldProps {
    label: string;
    value: string;
    editable?: boolean;
    field?: keyof typeof editedData;
    isEditing: boolean;
    onChangeValue: (field: string, value: string) => void;
}

const InfoField: React.FC<InfoFieldProps> = ({
    label,
    value,
    editable = false,
    field,
    isEditing,
    onChangeValue
}) => {
    // Mantener el estado local del input
    const [inputValue, setInputValue] = useState(value);

    const handleChangeText = (text: string) => {
        // Actualizar el estado local primero
        setInputValue(text);
        // Luego actualizar el estado padre
        if (field) {
            onChangeValue(field, text);
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.label}>{label}</Text>
            {isEditing && editable ? (
                <TextInput
                    value={inputValue}
                    onChangeText={handleChangeText}
                    placeholder={`Ingrese ${label.toLowerCase()}`}
                    placeholderTextColor="#666"
                    style={styles.input}
                />
            ) : (
                <Text style={styles.value}>{value}</Text>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        marginBottom: 10,
    },
    label: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 5,
    },
    input: {
        borderWidth: 1,
        borderColor: '#ddd',
        padding: 8,
        borderRadius: 4,
    },
    value: {
        fontSize: 16,
    },
});

export default InfoField;