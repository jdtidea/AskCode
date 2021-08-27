import {MsGraphApiCall} from './MsGraphApiCall';

class MsGraphService {
  static async search() {
    const config = {
      method: 'GET',
      url: `/me`,
      headers: {
        accept: 'application/json',
      },
    };

    let _result;

    _result = await MsGraphApiCall(config).catch((error) => {
      if (error.response) {
        console.log('ERR: Search Service: ', error.response);
        throw error.response.data;
      }
    });

    console.log('_result is ', _result);

    if (_result.status === 200) {
      return _result.data;
    } else {
      console.log('Invalid response code: ' + _result.status);
      throw new Error('Invalid response code: ' + _result.status);
    }
  }

  static async update(obj) {
    const config = {
      method: 'patch',
      url: `/me`,
      headers: {
        accept: 'application/json',
      },
      data: obj,
    };

    console.log(config);

    const _result = await MsGraphApiCall(config).catch((error) => {
      if (error.response) {
        console.log('ERR: Search Service: ', error.response);
        throw error.response.data;
      }
    });

    console.log('_result is update', _result);
  }
}

export {MsGraphService};
