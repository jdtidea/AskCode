import styled from 'styled-components';
import {QuestionIcon} from 'assets';
import {spacing, theme} from 'styles';
import {Banner} from 'components';
import {Grid} from 'layout';

const Wrapper = styled(Grid)`
  display: flex;
  text-align: left;
  margin-top: -${spacing.bannerHeight} !important;
  height: ${spacing.bannerHeight} !important;
  padding: 0;
  align-items: center;
  justify-content: flex-start;
`;

const AnswerText = styled.h3`
  margin: 0;
  font-size: ${theme.fontSizeH3};
  font-weight: ${theme.fontWeightH3};
  line-height: 1.5;
  color: ${theme.colorTextInverse};
`;

const QuestionImage = styled.img.attrs({
  src: QuestionIcon,
  alt: 'Question',
})`
  height: 36px;
  width: 36px;
  margin-right: ${theme.spacingXS};
`;

interface IAnswerHeader {
  query: string | null | undefined;
}

export function AnswerHeader({query}: IAnswerHeader) {
  return (
    <>
      <Banner />
      <Wrapper>
        <div className="row">
          <div className="col-12" style={{display: 'inline-flex'}}>
            <QuestionImage />
            <AnswerText>Your answer to: "{query}"</AnswerText>
          </div>
        </div>
      </Wrapper>
    </>
  );
}
