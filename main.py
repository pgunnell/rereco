from core.controller.campaign_controller import CampaignController

campaign_controller = CampaignController()

campaign_controller.create_campaign({'prepid': 'FirstCampaign'})
campaign = campaign_controller.get_campaign('FirstCampaign')
print(campaign)
campaign.set('memory', 4000)
campaign.set('notes', 'Note note note.')
campaign.set('history', [])
campaign_controller.update_campaign(campaign.json())
campaign = campaign_controller.get_campaign('FirstCampaign')
print(campaign)
