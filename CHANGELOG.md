# [1.2.0](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/compare/v1.1.1...v1.2.0) (2021-03-30)


### Features

* **api-client:** add getter for match history ([d5648d0](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/d5648d02842847157b689cfc94fd2c1697d47969))
* **session-analyzer:** add class for analysis on a stream session ([7602379](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/76023795842060d52a07d140cf50645364fd31f8))
* **session-analyzer:** add session-analyzer and session-start commands ([28a24b6](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/28a24b654ac60187e4462b2e68bd189a1c9303db))




## [1.1.1](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/compare/v1.1.0...v1.1.1) (2021-03-21)


### Bug Fixes

* **settings:** allow accents on settings ([8b01224](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/8b01224ed12b70995140e9e4b21a5ef0b4478761))




# [1.1.0](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/compare/v1.0.0...v1.1.0) (2021-03-09)


### Features

* **core:** add check for new version at startup ([1958157](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/19581572fc69bd6c4afacb9d44eb5d57a527d305))




# [1.0.0](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/compare/v0.3.1...v1.0.0) (2021-02-27)


### Bug Fixes

* **settings:** load initial settings file if exists on init ([757aa32](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/757aa32b0dbc5015d22bb18ad85e3c49eb8e1eb2))


### Features

* **api-client:** add faceit api client class ([8ae61c9](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/8ae61c909edd9e130d7ff068de5f8fc1c30a1848))
* **command:** add command executor ([10df0c5](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/10df0c5b26cd1f76425b6a37de09485da4e3e66e))
* **commands:** add faceit elo command to ui settings ([345829c](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/345829c1a9302ba9f0e890b5a49dd40f8196d8ea))
* **core:** add messaging module and default error messages ([c323806](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/c323806174e6cea99b6a9fbc13c2f0aec88cc84b))
* **core:** add settings manager ([5832bba](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/5832bbad32ca5df27004d32dd683a5e93cc52ef5))
* **core:** enable get elo command ([17642b5](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/17642b5c6c7a41a7d28b649e70db73bc3f7d47fb))
* **core:** remove unnecessary import ([331cefd](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/331cefdaea27a2cb75edd50be3ac0d7a4b7a9dd5))
* **core:** validate settings after saving them ([e7cdb8d](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/e7cdb8da8d8c81105b35a4315dd33f16943ebd17))
* **refactor:** removed all previous files and re-design directory access pattern ([9bae564](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/9bae5648a83f42b7eeb85977a78de47d75e0a7b9))
* **settings:** add appropriate params to save on script Init and ReloadSettings ([887d1fe](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/887d1fe6c8e552ecb3e1a8b7024eba65f3a9dc6b))
* **settings:** add get_commands method to settings class ([aca1b9b](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/aca1b9b0ec6964c68757aa9df94524334e01d608))
* **settings:** add validation for required fields method ([36d4d06](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/36d4d068c61e1f6d3b6e1c5a25d448a232b59da2))
* **settings:** save new settings on clicking the save settings ui button ([ddec115](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/ddec1151b6b0232f449d00ea4719a8e94b1929a0))
* **ui-config:** add faceit api key setting ([e2ed7e3](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/e2ed7e31e4afd67fef6550f0c7f80e04af569024))
* **ui-config:** add general messages and modify name for default argument ([f75d369](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/f75d369070b9c4867629ebbf981c88177729049a))
* **ui-config:** update string for faceit elo message ([3b7d1b0](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/3b7d1b0ff53edeac9a82c5937ac1adef625af7c4))


### BREAKING CHANGES

* **commands:**  is replaced in ELO Check Command for 
* **settings:** get_commands now returns a dictionary with the name of the command and the value for it stored in settings
* **ui-config:** default_user for commands is now called default_argument




## [0.3.1](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/compare/v0.3.0...v0.3.1) (2021-02-16)


### Bug Fixes

* **settings:** set correct label and tooltip for permission error message ([f052c0e](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/f052c0eaee35055f7e6a04a1018e42af1c36c16d))




# [0.3.0](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/compare/v0.2.0...v0.3.0) (2021-02-16)


### Bug Fixes

* **settings:** update dictionary instead of setting attributes on reset_settings method ([153f406](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/153f4067286edae0e58fdebfe7b67227091b15d2))


### Features

* **core:** check if the user has permission to run a command before executing it ([50d8141](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/50d8141703ab950aa960e0657433e5d1bf7bcd2b))
* **ui-settings:** add faceitPermissionSettings to common messages section ([083c006](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/083c00639f07264f1d3021c8d3d5f09f3b2bd95a))




# [0.2.0](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/compare/v0.1.0...v0.2.0) (2021-02-16)


### Bug Fixes

* **core:** revert version to the right one ([43ddc0c](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/43ddc0c7b2d15c27000a846038ef6277f89019f9))
* **ui-config:** modify wrong string ([5050af7](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/5050af7c62e35c1305baf431859006a84d2fa46e))
* **workflow:** do not push new commits if there is no new version ([e643e56](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/e643e56b37d59f01db2f727a85f2c00e3eae6a77))
* **workflow:** fix quotes ([7fe205e](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/7fe205e2c1eb5c6a287076e6b66a012a61367136))


### Features

* **core:** add check for user cooldown in commands ([c8a884a](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/c8a884a1b8cae379702578da4f030fa5a2d994d1))





# [0.1.0](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/compare/v0.0.0...v0.1.0) (2021-02-16)


### Features

* **core:** initial version of this script ([1bccc0c](https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/commit/1bccc0ca165541f9f448e693db22321064e74743))




