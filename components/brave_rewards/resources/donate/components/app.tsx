/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

import * as React from 'react'
import { bindActionCreators, Dispatch } from 'redux'
import { connect } from 'react-redux'

// Components
import DonateToSite from './donateToSite'
import DonateToTwitterUser from './donateToTwitterUser'

// Utils
import * as rewardsActions from '../actions/donate_actions'

interface DonationDialogArgs {
  publisherKey: string
  tweetMetaData?: RewardsDonate.TweetMetaData
}

interface Props extends RewardsDonate.ComponentProps {
  dialogArgs: DonationDialogArgs
}

export class App extends React.Component<Props, {}> {

  get actions () {
    return this.props.actions
  }

  isTwitterAccount = (publisherKey: string) => {
    return /^twitter#channel:[0-9]+$/.test(publisherKey)
  }

  render () {
    const { publishers } = this.props.rewardsDonateData

    if (!publishers) {
      return null
    }

    const publisherKey = this.props.dialogArgs.publisherKey
    const publisher = publishers[publisherKey]

    if (!publisher) {
      return null
    }

    let donation
    if (this.isTwitterAccount(publisherKey)) {
      const tweetMetaData = this.props.dialogArgs.tweetMetaData
      if (tweetMetaData) {
        donation = (
          <DonateToTwitterUser
            publisher={publisher}
            tweetMetaData={tweetMetaData}
          />
        )
      }
    } else {
      donation = (
        <DonateToSite
          publisher={publisher}
        />
      )
    }

    return (
      <div>
        {donation}
      </div>
    )
  }
}

export const mapStateToProps = (state: RewardsDonate.ApplicationState) => ({
  rewardsDonateData: state.rewardsDonateData
})

export const mapDispatchToProps = (dispatch: Dispatch) => ({
  actions: bindActionCreators(rewardsActions, dispatch)
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(App)
