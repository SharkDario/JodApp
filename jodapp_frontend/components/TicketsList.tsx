// components/TicketsList.tsx
/*
import React, { useEffect, useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    SectionList,
    RefreshControl,
    SafeAreaView,
} from 'react-native';
import { useAuth } from '@/context/AuthContext';
import VerificationModal from './VerificationModal';

interface Ticket {
    id: number;
    tipo: string;
    nombre?: string;
    fiesta?: string;
    categoria?: string;
    cantidad: number;
}

interface TicketItemProps {
    ticket: Ticket;
    onCanjear: () => void;
}

const TicketItem: React.FC<TicketItemProps> = ({ ticket, onCanjear }) => (
    <View style={styles.ticketContainer}>
        <View style={styles.ticketInfo}>
            <Text style={styles.ticketTitle}>
                {ticket.tipo === 'articulo' ? ticket.nombre : `${ticket.fiesta} - ${ticket.categoria}`}
            </Text>
            <Text style={styles.ticketQuantity}>Cantidad: {ticket.cantidad}</Text>
        </View>
    </View>
);

interface TicketsListProps {
    onTicketSelect?: (ticket: Ticket) => void;
}

const TicketsList: React.FC<TicketsListProps> = ({ onTicketSelect }) => {
    const { tickets = { articulos: [], entradas: [] }, loadTickets, confirmarCanje } = useAuth();
    const [refreshing, setRefreshing] = useState(false);
    const [showVerificationModal, setShowVerificationModal] = useState(false);
    const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);

    useEffect(() => {
        if (loadTickets) {
            loadTickets();
        }
    }, [loadTickets]);

    const handleRefresh = async () => {
        setRefreshing(true);
        try {
            if (loadTickets) {
                await loadTickets();
            }
        } finally {
            setRefreshing(false);
        }
    };

    const handleCanjear = (ticket: Ticket) => {
        if (onTicketSelect) {
            onTicketSelect(ticket);
        } else {
            setSelectedTicket(ticket);
            setShowVerificationModal(true);
        }
    };

    const handleVerify = async (codigo: string) => {
        if (!selectedTicket || !confirmarCanje) return;

        try {
            await confirmarCanje(selectedTicket.id, selectedTicket.tipo, codigo);
            setShowVerificationModal(false);
            setSelectedTicket(null);
        } catch (error) {
            console.error('Error al confirmar canje:', error);
        }
    };

    const sections = [
        { title: 'Entradas', data: tickets.entradas || [] },
        { title: 'Bebidas', data: tickets.articulos || [] },
    ];

    const renderTicketItem = ({ item }: { item: Ticket }) => (
        <TicketItem ticket={item} onCanjear={() => handleCanjear(item)} />
    );

    return (
        <SafeAreaView style={styles.container}>
            <SectionList
                sections={sections}
                keyExtractor={(item) => `${item.tipo}-${item.id}`}
                renderItem={renderTicketItem}
                renderSectionHeader={({ section: { title } }) => (
                    <Text style={styles.sectionHeader}>{title}</Text>
                )}
                contentContainerStyle={styles.listContent}
                refreshControl={
                    <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
                }
                ListEmptyComponent={
                    <View style={styles.emptyContainer}>
                        <Text style={styles.emptyText}>No tienes tickets disponibles</Text>
                    </View>
                }
            />

            {showVerificationModal && (
                <VerificationModal
                    visible={showVerificationModal}
                    onClose={() => {
                        setShowVerificationModal(false);
                        setSelectedTicket(null);
                    }}
                    onVerify={handleVerify}
                    ticketInfo={selectedTicket}
                />
            )}
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'black',
    },
    listContent: {
        flexGrow: 1,
        paddingVertical: 8,
    },
    emptyContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    sectionHeader: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#fff',
        backgroundColor: '#333',
        paddingHorizontal: 16,
        paddingVertical: 8,
    },
    ticketContainer: {
        backgroundColor: '#ffffff',
        marginHorizontal: 16,
        marginVertical: 8,
        borderRadius: 8,
        padding: 16,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        elevation: 2,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
    },
    ticketInfo: {
        flex: 1,
    },
    ticketTitle: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 4,
    },
    ticketQuantity: {
        fontSize: 14,
        color: '#666',
    },
    emptyText: {
        textAlign: 'center',
        marginTop: 32,
        fontSize: 16,
        color: '#666',
    },
});

export default TicketsList;
*/

// components/TicketsList.tsx

import React, { useEffect, useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    FlatList,
    RefreshControl,
    SafeAreaView,
} from 'react-native';
import { useAuth } from '@/context/AuthContext';
import VerificationModal from './VerificationModal';

interface Ticket {
    id: number;
    tipo: string;
    nombre?: string;
    fiesta?: string;
    categoria?: string;
    cantidad: number;
}

interface TicketItemProps {
    ticket: Ticket;
    onCanjear: () => void;
}

const TicketItem: React.FC<TicketItemProps> = ({ ticket, onCanjear }) => {
    return (
        <View style={styles.ticketContainer}>
            <View style={styles.ticketInfo}>
                <Text style={styles.ticketTitle}>
                    {ticket.tipo === 'articulo' ? ticket.nombre : `${ticket.fiesta} - ${ticket.categoria}`}
                </Text>
                <Text style={styles.ticketQuantity}>Cantidad: {ticket.cantidad}</Text>
            </View>
            {/* 
            <TouchableOpacity
                style={styles.canjearButton}
                onPress={onCanjear}
            >
                <Text style={styles.canjearButtonText}>Canjear</Text>
            </TouchableOpacity>
            */}
        </View>
    );
};

interface TicketsListProps {
    onTicketSelect?: (ticket: Ticket) => void;
}

const TicketsList: React.FC<TicketsListProps> = ({ onTicketSelect }) => {
    const { tickets = { articulos: [], entradas: [] }, loadTickets, confirmarCanje } = useAuth();
    const [refreshing, setRefreshing] = useState(false);
    const [showVerificationModal, setShowVerificationModal] = useState(false);
    const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);

    useEffect(() => {
        if (loadTickets) {
            loadTickets();
        }
    }, [loadTickets]);

    const handleRefresh = async () => {
        setRefreshing(true);
        try {
            if (loadTickets) {
                await loadTickets();
            }
        } finally {
            setRefreshing(false);
        }
    };

    const handleCanjear = (ticket: Ticket) => {
        if (onTicketSelect) {
            onTicketSelect(ticket);
        } else {
            setSelectedTicket(ticket);
            setShowVerificationModal(true);
        }
    };

    const handleVerify = async (codigo: string) => {
        if (!selectedTicket || !confirmarCanje) return;

        try {
            await confirmarCanje(
                selectedTicket.id,
                selectedTicket.tipo,
                codigo
            );
            setShowVerificationModal(false);
            setSelectedTicket(null);
        } catch (error) {
            console.error('Error al confirmar canje:', error);
        }
    };

    const ticketsData = React.useMemo(() => {
        const articulos = tickets?.articulos || [];
        const entradas = tickets?.entradas || [];
        return [...articulos, ...entradas];
    }, [tickets?.articulos, tickets?.entradas]);

    const renderTicketItem = ({ item }: { item: Ticket }) => (
        <TicketItem
            ticket={item}
            onCanjear={() => handleCanjear(item)}
        />
    );

    return (
        <SafeAreaView style={styles.container}>
            <FlatList
                data={ticketsData}
                renderItem={renderTicketItem}
                keyExtractor={(item) => `${item.tipo}-${item.id}`}
                contentContainerStyle={styles.listContent}
                refreshControl={
                    <RefreshControl
                        refreshing={refreshing}
                        onRefresh={handleRefresh}
                    />
                }
                ListEmptyComponent={
                    <View style={styles.emptyContainer}>
                        <Text style={styles.emptyText}>No tienes tickets disponibles</Text>
                    </View>
                }
            />

            {showVerificationModal && (
                <VerificationModal
                    visible={showVerificationModal}
                    onClose={() => {
                        setShowVerificationModal(false);
                        setSelectedTicket(null);
                    }}
                    onVerify={handleVerify}
                    ticketInfo={selectedTicket}
                />
            )}
        </SafeAreaView>
    );
};
const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'black',
    },
    listContent: {
        flexGrow: 1,
        paddingVertical: 8,
    },
    emptyContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    ticketContainer: {
        backgroundColor: '#ffffff',
        marginHorizontal: 16,
        marginVertical: 8,
        borderRadius: 8,
        padding: 16,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        elevation: 2,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
    },
    ticketInfo: {
        flex: 1,
    },
    ticketTitle: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 4,
    },
    ticketQuantity: {
        fontSize: 14,
        color: '#666',
    },
    canjearButton: {
        backgroundColor: '#4CAF50',
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 4,
        marginLeft: 16,
    },
    canjearButtonText: {
        color: '#ffffff',
        fontWeight: 'bold',
    },
    emptyText: {
        textAlign: 'center',
        marginTop: 32,
        fontSize: 16,
        color: '#666',
    },
});

export default TicketsList;

/*
import React, { useEffect, useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    FlatList,
    RefreshControl,
} from 'react-native';
import { useAuth } from '@/context/AuthContext';
import VerificationModal from './VerificationModal';

interface TicketItemProps {
    ticket: {
        id: number;
        tipo: string;
        nombre?: string;
        fiesta?: string;
        categoria?: string;
        cantidad: number;
    };
    onCanjear: () => void;
}

const TicketItem: React.FC<TicketItemProps> = ({ ticket, onCanjear }) => {
    return (
        <View style={styles.ticketContainer}>
            <View style={styles.ticketInfo}>
                <Text style={styles.ticketTitle}>
                    {ticket.tipo === 'articulo' ? ticket.nombre : `${ticket.fiesta} - ${ticket.categoria}`}
                </Text>
                <Text style={styles.ticketQuantity}>Cantidad: {ticket.cantidad}</Text>
            </View>
            <TouchableOpacity
                style={styles.canjearButton}
                onPress={onCanjear}
            >
                <Text style={styles.canjearButtonText}>Canjear</Text>
            </TouchableOpacity>
        </View>
    );
};

interface TicketsListProps {
    onTicketSelect?: (ticket: any) => void;
}

const TicketsList: React.FC<TicketsListProps> = ({ onTicketSelect }) => {
    const { tickets, loadTickets, confirmarCanje } = useAuth();
    const [refreshing, setRefreshing] = useState(false);
    const [showVerificationModal, setShowVerificationModal] = useState(false);
    const [selectedTicket, setSelectedTicket] = useState(null);

    useEffect(() => {
        loadTickets();
    }, []);

    const handleRefresh = async () => {
        setRefreshing(true);
        try {
            await loadTickets();
        } finally {
            setRefreshing(false);
        }
    };

    const handleCanjear = (ticket) => {
        if (onTicketSelect) {
            onTicketSelect(ticket);
        }
    };

    const handleVerify = async (codigo: string) => {
        if (!selectedTicket) return;

        await confirmarCanje(
            selectedTicket.id,
            selectedTicket.tipo,
            codigo
        );
        setShowVerificationModal(false);
        setSelectedTicket(null);
    };

    const renderTicketItem = ({ item }) => (
        <TicketItem
            ticket={item}
            onCanjear={() => handleCanjear(item)}
        />
    );

    return (
        <View style={styles.container}>
            <FlatList
                data={[...tickets.articulos, ...tickets.entradas]}
                renderItem={renderTicketItem}
                keyExtractor={(item) => `${item.tipo}-${item.id}`}
                refreshControl={
                    <RefreshControl
                        refreshing={refreshing}
                        onRefresh={handleRefresh}
                    />
                }
                ListEmptyComponent={
                    <Text style={styles.emptyText}>No tienes tickets disponibles</Text>
                }
            />

            <VerificationModal
                visible={showVerificationModal}
                onClose={() => {
                    setShowVerificationModal(false);
                    setSelectedTicket(null);
                }}
                onVerify={handleVerify}
                ticketInfo={selectedTicket}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5',
    },
    ticketContainer: {
        backgroundColor: '#ffffff',
        marginHorizontal: 16,
        marginVertical: 8,
        borderRadius: 8,
        padding: 16,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        elevation: 2,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
    },
    ticketInfo: {
        flex: 1,
    },
    ticketTitle: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 4,
    },
    ticketQuantity: {
        fontSize: 14,
        color: '#666',
    },
    canjearButton: {
        backgroundColor: '#4CAF50',
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 4,
        marginLeft: 16,
    },
    canjearButtonText: {
        color: '#ffffff',
        fontWeight: 'bold',
    },
    emptyText: {
        textAlign: 'center',
        marginTop: 32,
        fontSize: 16,
        color: '#666',
    },
});

export default TicketsList;*/