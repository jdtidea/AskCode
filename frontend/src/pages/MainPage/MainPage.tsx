import './MainPage.scss';
import {useCallback} from 'react';
import {LogoInverse, HomeBGFull, HomeBGSmall} from 'assets';
import {Background, SearchCard} from 'components';
import {useHistory} from 'react-router-dom';
import {theme} from 'styles';
import {Grid} from 'layout';
import styled from 'styled-components';

const Title = styled.h1`
  font-weight: bold;
  font-size: 4.5rem;
  line-height: 1;
  color: ${theme.colorTextInverse};
  text-align: left;
  margin-bottom: 0;
`;

const Footer = styled.div`
  display: flex;
  color: ${theme.colorTextInverse};
  font-size: ${theme.fontSizeBase};
  font-weight: ${theme.fontWeightBase};
  line-height: 1.5;
`;

export function MainPage() {
  const history = useHistory();

  const submitHandler = useCallback(
    (query: string) => {
      history.push({
        pathname: '/search',
        search: `?q=${query}`,
      });
    },
    [history],
  );

  return (
    <>
      <Background fullImage={HomeBGFull} smallImage={HomeBGSmall} withWave />
      <Grid>
        <div className="row">
          <div className="col-12">
            <Title>
              Let us find
              <br />
              the answers.
            </Title>
          </div>
        </div>
        <div className="row">
          <div className="col-12">
            <SearchCard onSubmit={submitHandler} />

            <Footer>
              <div className="row footer-container">
                <div className="col-l-2 col-s-12 ask-logo-container">
                  <img
                    alt="Ask Optum"
                    className="ask-logo"
                    style={{marginRight: '8px', width: '100px', height: '32px'}}
                    src={LogoInverse}
                  />
                </div>
                <div className="col-l-10 col-s-12">
                  <span className="footer-txt">
                    getting you the answers you need, wherever you are.
                  </span>
                </div>
              </div>
            </Footer>
          </div>
          <div className="col-2"></div>
        </div>
      </Grid>
    </>
  );
}
