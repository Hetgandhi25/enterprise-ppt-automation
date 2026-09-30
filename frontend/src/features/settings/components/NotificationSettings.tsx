import { useSettingsStore } from "../../../stores/useSettingsStore";

export function NotificationSettings() {
  const { enableNotifications, successToasts, failureToasts, desktopNotifications, updateSettings } = useSettingsStore();

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium text-foreground">Notifications</h3>
        <p className="text-sm text-muted-foreground">Manage how you are alerted about pipeline events.</p>
      </div>

      <div className="space-y-6 max-w-xl">
        <label className="flex items-start gap-3 cursor-pointer group">
          <input 
            type="checkbox" 
            checked={enableNotifications}
            onChange={(e) => updateSettings({ enableNotifications: e.target.checked })}
            className="rounded text-primary focus:ring-primary w-4 h-4 mt-0.5"
          />
          <div>
            <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">Enable Notifications</p>
            <p className="text-xs text-muted-foreground">Global toggle for all application alerts.</p>
          </div>
        </label>

        <div className={`space-y-4 pt-4 border-t border-border ${!enableNotifications && 'opacity-50 pointer-events-none'}`}>
          <label className="flex items-start gap-3 cursor-pointer group">
            <input 
              type="checkbox" 
              checked={successToasts}
              onChange={(e) => updateSettings({ successToasts: e.target.checked })}
              className="rounded text-primary focus:ring-primary w-4 h-4 mt-0.5"
            />
            <div>
              <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">Success Toasts</p>
              <p className="text-xs text-muted-foreground">Show in-app toast when a job completes successfully.</p>
            </div>
          </label>

          <label className="flex items-start gap-3 cursor-pointer group">
            <input 
              type="checkbox" 
              checked={failureToasts}
              onChange={(e) => updateSettings({ failureToasts: e.target.checked })}
              className="rounded text-primary focus:ring-primary w-4 h-4 mt-0.5"
            />
            <div>
              <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">Failure Toasts</p>
              <p className="text-xs text-muted-foreground">Show in-app toast when a job fails or errors out.</p>
            </div>
          </label>

          <label className="flex items-start gap-3 cursor-pointer group">
            <input 
              type="checkbox" 
              checked={desktopNotifications}
              onChange={(e) => updateSettings({ desktopNotifications: e.target.checked })}
              className="rounded text-primary focus:ring-primary w-4 h-4 mt-0.5"
            />
            <div>
              <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">Desktop Notifications</p>
              <p className="text-xs text-muted-foreground">Send native OS notifications for background tasks.</p>
            </div>
          </label>
        </div>
      </div>
    </div>
  );
}
