import styled from 'styled-components';
import {PropsWithChildren} from 'react';

interface IGrid {
  maxWidth?: number;
}

const GridComponent = styled.div.attrs({className: 'grid'})<{maxWidth: number}>`
  max-width: ${(p) => p.maxWidth}px;
`;
export function Grid({
  maxWidth = 1140,
  children,
  ...rest
}: PropsWithChildren<IGrid>) {
  return (
    <GridComponent {...rest} maxWidth={maxWidth}>
      {children}
    </GridComponent>
  );
}
