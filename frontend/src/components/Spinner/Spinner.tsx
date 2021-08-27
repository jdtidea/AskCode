import CircularProgress from '@material-ui/core/CircularProgress';
import {makeStyles} from '@material-ui/core/styles';
import {theme as uitkTheme} from 'styles';

const useStyles = makeStyles((theme) => ({
  spinner: {
    color: `${theme.palette.primary.main}`,
    marginTop: uitkTheme.spacingLG,
  },
}));

export function Spinner() {
  const classes = useStyles();

  return <CircularProgress className={classes.spinner} />;
}
