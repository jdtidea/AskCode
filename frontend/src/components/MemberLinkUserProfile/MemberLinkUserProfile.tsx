import './MemberLinkUserProfile.scss';
import styled from 'styled-components';
import {theme} from 'styles';
import {FeedbackButton} from '../Button/FeedbackButton';
import {Feedback} from 'types';
import React, {useState} from 'react';
import {HelperText, Label, TextInput, Button, Card, Text} from '@uitk/react';
import {MemberImage, GroupImage} from 'assets';
import {MsGraphService} from 'helpers';
import {Dialog} from '@uitk/react';
import {useMsal, useIsAuthenticated} from '@azure/msal-react';
import {HealthDataExchange as Icon1} from '@uitk/react-icons';

export function MemberLinkUserProfile() {
  const {instance} = useMsal();
  const activeAccount: any = instance.getActiveAccount();
  const [dateValue, setdateValue] = useState('');
  const [memberValue, setMemberValue] = useState('');
  const [customerValue, setCustomerValue] = useState('');

  const [isOpen, setIsOpen] = useState(false);
  const dismiss = () => setIsOpen(false);

  const [isOpenUnlink, setIsOpenUnlink] = useState(false);
  const dismissUnlink = () => setIsOpenUnlink(false);

  const onChange = (event) => {
    setdateValue(event.target.value);
  };

  const onMemberValueChange = (event) => {
    setMemberValue(event.target.value);
  };

  const onCustumerValueChange = (event) => {
    setCustomerValue(event.target.value);
  };

  const onSearchBtnClicked = async () => {
    fetchUser();
  };

  const onUnlinkBtnClicked = async () => {
    setIsOpenUnlink(false);
  };

  const VisuallyHidden = styled.span`
    clip: rect(0 0 0 0);
    clip-path: inset(50%);
    height: 1px;
    overflow: hidden;
    position: absolute;
    white-space: nowrap;
    width: 1px;
  `;
  const HealthDataExchange = styled(Icon1)`
    height: ${theme.spacingM};
    width: ${theme.spacingM};
  `;

  const fetchUser = async () => {
    let _result = await MsGraphService.search().catch((e) => {
      console.log('ERROR at Results page ', e);
      return;
    });
    // setMemberValue(_result.displayName);
    // setdateValue(_result.surname);
    // setCustomerValue(_result.userPrincipalName);
    console.log(_result);
    setMemberValue(_result.extension_f3fb518578a34f3fb90c54fd4c3eee46_MemberID);
    setCustomerValue(
      _result.extension_f3fb518578a34f3fb90c54fd4c3eee46_GroupNumber,
    );
    setdateValue(
      _result.extension_f3fb518578a34f3fb90c54fd4c3eee46_DateofBirth,
    );
    setIsOpen(true);
    console.log('----------', _result);
  };

  const onSaveBtnClicked = async () => {
    updateUser();
  };

  const updateUser = async () => {
    // let updateUser = {
    //     preferredLanguage : memberValue,
    //     officeLocation : customerValue,
    //     jobTitle : dateValue,
    // }
    let updateUser = {
      extension_f3fb518578a34f3fb90c54fd4c3eee46_MemberID: memberValue,
      extension_f3fb518578a34f3fb90c54fd4c3eee46_GroupNumber: customerValue,
      extension_f3fb518578a34f3fb90c54fd4c3eee46_DateofBirth: dateValue,
    };
    let _result = await MsGraphService.update(updateUser).catch((e) => {
      console.log('ERROR at Results page ', e);
      return;
    });

    setIsOpen(false);
    console.log('----------', _result);
  };
  //if (!activeAccount?.idTokenClaims?.extension_MemberID) {
  let extension_MemberID = false;
  let extension_MemberID_1 = '123';
  if (extension_MemberID) {
    return (
      <Card
        header={
          <h2>
            Your healthcare information is <b>not linked</b>.
          </h2>
        }
        className="member-link-card"
        icon={<HealthDataExchange size={'m'} />}>
        <Button onPress={() => setIsOpen(true)} className="link-btn-up">
          <span>Link</span>
          <VisuallyHidden>Opens Modal Window</VisuallyHidden>
        </Button>

        {isOpen && (
          <Dialog
            isOpen={isOpen}
            title="Link your information"
            closeButtonText="X"
            isDismissable
            className="dialog-member-link"
            onClose={dismiss}>
            <Dialog.Body>
              <Text>
                <br />
                <span className="sub-text">
                  By linking your healthcare information, Optum can provide you
                  with better aswers faster than ever!
                </span>
                <span className="sub-text">
                  This enables us to gather information on your behalf from
                  across the enterprise.
                </span>

                <form className="align">
                  <div className="row">
                    <div className="col-4">
                      <Label style={{display: 'flex'}}>Member ID</Label>
                      <TextInput
                        value={memberValue}
                        onChange={onMemberValueChange}
                      />
                    </div>
                    <div className="col-4">
                      <img
                        className="demo-img"
                        alt="Member"
                        src={MemberImage}
                      />
                    </div>
                  </div>
                  <div className="row">
                    <div className="col-4">
                      <Label style={{display: 'flex'}}>Group Number</Label>
                      <TextInput
                        value={customerValue}
                        onChange={onCustumerValueChange}
                      />
                    </div>
                    <div className="col-4">
                      <img className="demo-img" alt="Group" src={GroupImage} />
                    </div>
                  </div>
                  <div className="row">
                    <div className="col-3">
                      <div className="date-input-holder">
                        <Label style={{display: 'flex'}}>Date Of Birth</Label>
                        <HelperText style={{display: 'flex'}}>
                          MM/DD/YYYY
                        </HelperText>
                        <TextInput value={dateValue} onChange={onChange} />
                      </div>
                    </div>
                  </div>
                </form>
              </Text>
            </Dialog.Body>
            <Dialog.Actions>
              <Button onPress={onSaveBtnClicked}>Save & link</Button>
              <Button variant="ghost" onPress={dismiss}>
                Cancel
              </Button>
            </Dialog.Actions>
          </Dialog>
        )}
      </Card>
    );
  } else {
    return (
      <Card
        header={
          <h2>
            Your healthcare information is <b>successfully linked</b>.
          </h2>
        }
        subheader={<h2>Member ID : {extension_MemberID_1}</h2>}
        className="member-link-card"
        icon={<HealthDataExchange size={'m'} />}>
        <Button onPress={onSearchBtnClicked} className="link-btn-ud">
          <span>Update Details</span>
          <VisuallyHidden>Opens Modal Window</VisuallyHidden>
        </Button>
        &nbsp;&nbsp;&nbsp;&nbsp;
        <Button onPress={() => setIsOpenUnlink(true)} className="link-btn-u">
          <span>Unlink</span>
          <VisuallyHidden>Opens Modal Window</VisuallyHidden>
        </Button>
        {isOpen && (
          <Dialog
            isOpen={isOpen}
            title="Update information"
            closeButtonText="X"
            isDismissable
            className="dialog-member-link"
            onClose={dismiss}>
            <Dialog.Body>
              <Text>
                <br />
                <span className="sub-text">
                  By linking your healthcare information, Optum can provide you
                  with better aswers faster than ever!
                </span>
                <span className="sub-text">
                  This enables us to gather information on your behalf from
                  across the enterprise.
                </span>

                <form className="align">
                  <div className="row">
                    <div className="col-4">
                      <Label style={{display: 'flex'}}>Member ID</Label>
                      <TextInput
                        value={memberValue}
                        onChange={onMemberValueChange}
                      />
                    </div>
                    <div className="col-4">
                      <img
                        className="demo-img"
                        alt="Member"
                        src={MemberImage}
                      />
                    </div>
                  </div>
                  <div className="row">
                    <div className="col-4">
                      <Label style={{display: 'flex'}}>Group Number</Label>
                      <TextInput
                        value={customerValue}
                        onChange={onCustumerValueChange}
                      />
                    </div>
                    <div className="col-4">
                      <img className="demo-img" alt="Group" src={GroupImage} />
                    </div>
                  </div>
                  <div className="row">
                    <div className="col-3">
                      <div className="date-input-holder">
                        <Label style={{display: 'flex'}}>Date Of Birth</Label>
                        <HelperText style={{display: 'flex'}}>
                          MM/DD/YYYY
                        </HelperText>
                        <TextInput value={dateValue} onChange={onChange} />
                      </div>
                    </div>
                  </div>
                </form>
              </Text>
            </Dialog.Body>
            <Dialog.Actions>
              <Button onPress={onSaveBtnClicked}>Save & link</Button>
              <Button variant="ghost" onPress={dismiss}>
                Cancel
              </Button>
            </Dialog.Actions>
          </Dialog>
        )}
        {isOpenUnlink && (
          <Dialog
            isOpen={isOpenUnlink}
            title="Unlink healthcare information"
            closeButtonText="X"
            isDismissable
            className="dialog-member-link"
            onClose={dismissUnlink}>
            <Dialog.Body>
              <Text>
                <br />
                <span className="sub-text">
                  Unlinking will mean AskOptum cannot provide you with
                  personalized answers.
                </span>
                <span className="sub-text">
                  Are you sure you want to unlink? You can re-link at any time.
                </span>
              </Text>
            </Dialog.Body>
            <Dialog.Actions>
              <Button onPress={onUnlinkBtnClicked}>Unlink</Button>
              <Button variant="ghost" onPress={dismissUnlink}>
                Cancel
              </Button>
            </Dialog.Actions>
          </Dialog>
        )}
      </Card>
    );
  }
}
