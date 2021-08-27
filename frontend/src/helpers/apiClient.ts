import axios from 'axios';
import StatusCodes from 'http-status-codes';
import {msalInstance} from 'auth';
import {config} from 'config';

interface IApiClientOptions {
  method?: 'POST' | 'GET' | 'PUT' | 'DELETE';
}

export async function apiClient(
  endpoint: string,
  {method = 'GET'}: IApiClientOptions,
) {
  const url = `/api/v1/${endpoint}`;
  const accounts = msalInstance.getAllAccounts();
  let headers = {};

  if (accounts.length > 0) {
    let msalResponse;
    try {
      msalResponse = await msalInstance.acquireTokenSilent({
        scopes: config.scopes,
        account: accounts[0],
      });
    } catch (e) {
      console.error('error getting access token ', e);
      msalResponse = await msalInstance.acquireTokenPopup({
        scopes: config.scopes,
        account: accounts[0],
      });
    }

    const token = msalResponse.accessToken;
    headers = {
      ...headers,
      Authorization: token ? `Bearer ${token}` : '',
    };
  }

  const requestConfig = {
    method,
    url,
    headers,
    validateStatus: () => true,
  };
  const response = await axios(requestConfig);

  if (
    response.status >= StatusCodes.OK &&
    response.status <= StatusCodes.PARTIAL_CONTENT
  ) {
    return {body: response.data, headers: response.headers};
  }
  return Promise.reject(response.data);
}
