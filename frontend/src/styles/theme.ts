import {optumSolas, UITKTheme} from '@uitk/themes';
import {createMuiTheme} from '@material-ui/core/styles';

// override any theme default properties here
const theme: UITKTheme = {
  ...optumSolas,
};

const muiTheme = createMuiTheme({
  palette: {
    primary: {
      light: '#E87722',
      main: '#C25608',
      dark: '#C25608',
    },
    secondary: {
      light: '#E87722',
      main: '#C25608',
      dark: '#C25608',
    },
    error: {
      light: '#FAEDEC',
      main: '#E32315',
      dark: '#E32315',
    },
    warning: {
      light: '#F3BC29',
      main: '#F3BC29',
      dark: '#F3BC29',
      contrastText: '#FFFFFF',
    },
    info: {
      light: '#078576',
      main: '#078576',
      dark: '#078576',
    },
    success: {
      light: '#627D32',
      main: '#627D32',
      dark: '#627D32',
    },
    text: {
      primary: '#282A2E',
      secondary: '#63666A',
      disabled: '#B1B2B3',
    },
    background: {
      paper: '#F7F7F7',
      default: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: "'Arial', 'Helvetica', 'sans-serif'",
  },
});

export {muiTheme, theme};
