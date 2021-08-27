import {useMemo} from 'react';
import {BrowserRouter, Route, Redirect, Switch} from 'react-router-dom';
import {MainPage, ProfilePage, ResultsPage} from 'pages';
import {Header} from 'components';
import {useUser} from 'auth';

function App() {
  const {inProgress, isAuthenticated} = useUser();
  const authenticatedRoutes = useMemo(() => {
    return isAuthenticated ? (
      <Route exact path="/profile" component={ProfilePage} />
    ) : null;
  }, [isAuthenticated]);
  return (
    <BrowserRouter>
      <Header />
      <Switch>
        <Route exact path="/" component={MainPage} />
        <Route exact path="/search" component={ResultsPage} />
        <Route exact path="/auth" component={MainPage} />
        {authenticatedRoutes}
        {inProgress === 'none' ? <Redirect to="/" /> : null}
      </Switch>
    </BrowserRouter>
  );
}

export default App;
