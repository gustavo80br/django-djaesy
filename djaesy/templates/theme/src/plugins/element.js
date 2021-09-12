import { ElButton, ElDatePicker, ElTooltip, ElPopover, ElNotification  } from 'element-plus'

export default (app) => {
  app.use(ElButton)
  app.use(ElDatePicker)
  app.use(ElTooltip)
  app.use(ElPopover)
  app.use(ElNotification)
}
