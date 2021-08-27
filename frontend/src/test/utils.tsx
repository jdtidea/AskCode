import {render} from '@testing-library/react';
import {ThemeProvider} from '@material-ui/core/styles';
import {muiTheme} from 'styles';
import {Toolkit} from '@uitk/react';
import {BrowserRouter} from 'react-router-dom';

function Providers({children}) {
  return (
    <Toolkit spacing grid>
      <ThemeProvider theme={muiTheme}>
        <BrowserRouter>{children}</BrowserRouter>
      </ThemeProvider>
    </Toolkit>
  );
}
const customRender = (ui: any, options: any = {}) => {
  return render(ui, {wrapper: Providers, ...options});
};

export * from '@testing-library/react';
export {customRender as render};
