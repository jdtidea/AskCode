import {Breadcrumbs} from '@material-ui/core';
import {Link} from 'react-router-dom';
import styled from 'styled-components';

const Wrapper = styled.div`
  padding-left: 32px;
  padding-top: 16px;
`;

export function BreadCrumbs() {
  return (
    <Wrapper>
      <Breadcrumbs separator="›" aria-label="breadcrumb">
        <Link to="/">Ask Optum</Link>
        <Link color="inherit" to="/profile">
          User Profile
        </Link>
      </Breadcrumbs>
    </Wrapper>
  );
}
