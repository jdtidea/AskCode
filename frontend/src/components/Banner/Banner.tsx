import styled from 'styled-components';
import {colors, spacing} from 'styles';

const Wrapper = styled.div`
  position: relative;
  display: flex;
  width: 100%;
  height: ${spacing.bannerHeight};
  z-index: -1;
`;
const StyledBanner = styled.div`
  width: 100%;
  height: 100%;
  background: ${colors.gradientPurpleOrange};
`;
export function Banner() {
  return (
    <Wrapper>
      <StyledBanner />
    </Wrapper>
  );
}
