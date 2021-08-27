import styled from 'styled-components';
import {theme} from 'styles';
import {Grid} from 'layout';

const Wrapper = styled.div.attrs({className: 'col-12'})`
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-top: ${theme.spacingSM};
  margin-bottom: ${theme.spacingSM};
  padding-left: ${theme.spacingM};
`;
export function NoResults() {
  return (
    <Grid>
      <div className="row">
        <Wrapper>
          <h3>
            Unfortunately, we were not able to find any answers to your
            question.
          </h3>
          <p>
            AskOptum is learning and improving constantly. We hope to be of
            better assistance to you soon.
          </p>
        </Wrapper>
      </div>
    </Grid>
  );
}
