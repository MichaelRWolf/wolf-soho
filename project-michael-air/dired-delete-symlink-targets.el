;;; dired-delete-symlink-targets.el --- delete/trash the real files a dired symlink points to

;; Not wired into any config yet -- for review.
;; Usage: in a dired buffer full of symlinks (e.g. messages_attachments/by_size/100M+/),
;; mark entries with `m` (or leave point on one with no marks), then M-x
;; mrw/dired-delete-symlink-targets (or bind it, e.g.):
;;   (define-key dired-mode-map (kbd "C-c C-k") #'mrw/dired-delete-symlink-targets)
;;
;; Deletes the TARGET the symlink points to (via Trash, so it's recoverable),
;; leaving the symlink itself in place -- it'll go dangling until the
;; create_by_size_symlinks script is rerun (which wipes and rebuilds by_size/
;; from scratch each time anyway).

(defun mrw/dired-delete-symlink-targets (&optional arg)
  "Trash the files that the marked (or current) dired symlinks point to.
With a prefix ARG, see `dired-get-marked-files' for its meaning."
  (interactive "P")
  (let* ((files (dired-get-marked-files nil arg))
         (targets (delq nil (mapcar (lambda (f)
                                       (and (file-symlink-p f)
                                            (file-chase-links f)))
                                     files))))
    (unless targets
      (user-error "No symlinks marked"))
    (when (yes-or-no-p (format "Trash %d target file(s)? " (length targets)))
      (dolist (target targets)
        (move-file-to-trash target))
      (message "Trashed %d target file(s)" (length targets))
      (revert-buffer))))

(provide 'dired-delete-symlink-targets)
;;; dired-delete-symlink-targets.el ends here
