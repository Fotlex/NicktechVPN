import apiClient from './apiClient';

export const fetchCurrentUser = async (startParam: string | null) => {
    const params = startParam !== null ? { start_param: startParam } : {};
    const response = await apiClient.get('users/current/', { params })
    return response.data;
};

export const claimGift = async () => {
    const response = await apiClient.post('users/claim-gift/')
    return response.data;
};

export const fetchVpnConfig = async () => {
    const response = await apiClient.get('users/vpn-config/');
    return response.data;
};