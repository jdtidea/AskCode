import './ResultsPage.scss';
import styled from 'styled-components';
import {useState, useEffect, useCallback, ChangeEvent, FormEvent} from 'react';
import {SearchResult, Spinner, LoginNotification} from 'components';
import {Grid} from 'layout';
import {NoResults, SearchBar} from './components';
import {useLocation, useHistory} from 'react-router-dom';
import {useSearch} from 'hooks';
import {BestAnswer} from 'assets';

const PageWrapper = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
`;

const BestAns = styled.img.attrs({src: BestAnswer, alt: 'Best Answer'})`
  width: 100%;
`;

export function ResultsPage() {
  const location = useLocation<{q: string}>();
  const history = useHistory();
  const query = new URLSearchParams(location.search).get('q');
  const {data, isLoading, refetch, isError} = useSearch(query);
  const [searchInput, setSearchInput] = useState<string>();

  // pre-populate search box on first load from query string
  useEffect(() => {
    if (query) {
      setSearchInput(query);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleChange = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => {
      setSearchInput(event.target.value);
    },
    [setSearchInput],
  );

  const submitHandler = useCallback(
    (e: FormEvent) => {
      e.preventDefault();
      if (searchInput) {
        history.push({search: `?q=${searchInput}`});
        if (searchInput === (query && decodeURIComponent(query))) {
          refetch();
        }
      }
    },
    [history, searchInput, query, refetch],
  );

  return (
    <PageWrapper>
      <SearchBar
        onSubmit={submitHandler}
        onChange={handleChange}
        value={searchInput}
      />
      {isLoading ? (
        <Spinner />
      ) : isError || data?.results.length === 0 ? (
        <NoResults />
      ) : (
        <>
          <Grid>
            <LoginNotification />
            {data ? (
              <div className="best-answer-container">
                <BestAns />
              </div>
            ) : null}
            {data?.results.map((result, index) => {
              return (
                <SearchResult
                  key={index}
                  index={index}
                  query={data.query}
                  traceId={data.traceId}
                  title={result.title}
                  url={result.url}
                  skill={result.skill}
                  domain={result.domain}
                  content={result.content}
                  variant={result.variant}
                  score={result.score}
                />
              );
            })}
          </Grid>
        </>
      )}
    </PageWrapper>
  );
}
