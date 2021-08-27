// import {loginRequest, graphConfig} from '../auth/config';
import {msalInstance} from 'auth';
import {config} from 'config';
import axios from 'axios';

/**
 * Create an Axios Client with defaults
 */
const getClient = (headers) => {
  return axios.create({
    baseURL: 'https://graph.microsoft.com/v1.0',
    headers,
  });
};

/**
 * Request Wrapper with default success/error actions
 */
const MsGraphApiCall = async function (options) {
  const accounts = msalInstance.getAllAccounts();

  let headers = {};

  if (accounts.length > 0) {
    console.log('account found');

    let response;
    try {
      response = await msalInstance.acquireTokenSilent({
        scopes: config.scopes,

        account: accounts[0],
      });
    } catch (e) {
      console.log('error getting access token ', e);
    }

    // const headers = new Headers();
    const bearer = `Bearer ${response.accessToken}`;

    headers = {
      Authorization: bearer,
    };
  } else if (options.url === '/search') {
    options.params.tu = true;
  }

  console.log('making request)');

  const client = getClient(headers);
  return client.request(options);
};

export {MsGraphApiCall};
